from pymongo import MongoClient
import logging

from config import MongoConfig

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class OtomotoPipeline:
    def process_item(self, item, spider):
        return item


class OtomotoMongoPipeline:
    mongo_db = MongoConfig()
    client = MongoClient(mongo_db.get_url())
    db = client[mongo_db.db_name]
    collection = db[mongo_db.collection]

    def __init__(self, last_price=None, _id=None):
        self.last_price = last_price
        self._id = _id

    def process_item(self, item, spider):
        logger.debug(f"Processing item: {item['id']}")
        if not self.is_car_exist(item):
            self.collection.insert_one(item)
            logger.debug(f"Car added to database: {item['id']}")
            return item
        else:
            if item["price"]["price"][0]['price'] != self.last_price:
                self.collection.update_one({'_id': self._id},
                                           {'$push': {'price.price': item['price']['price'][0]}})
                logger.debug(f"Price has changed for car: {item['id']}")
            else:
                logger.debug(f"Price has not changed for car: {item['id']}")
        return item

    def is_car_exist(self, item):
        car = None
        try:
            car = self.collection.find_one({'id': item['id']})
        except Exception as e:
            logging.error(f"Error: {e}. id: {item['id']} url: {item['url']}")
            return False
        finally:
            if car:
                self._id = car['_id']
            self.last_price = self.get_last_price(car['price']['price']) if car else None
            return True if car else False

    def get_last_price(self, data):
        sorted_prices = sorted(data, key=lambda x: x['time'], reverse=True)
        return sorted_prices[0]['price']
