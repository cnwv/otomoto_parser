from pymongo import MongoClient
import logging

logger = logging.getLogger('otomoto')


class OtomotoPipeline:
    def process_item(self, item, spider):
        return item


class OtomotoMongoPipeline:
    client = MongoClient("mongodb://root:example@localhost:27021")
    db = client["otomoto"]
    collection = db["otomoto"]

    def __init__(self, last_price=None, _id=None):
        self.last_price = last_price
        self._id = _id

    def process_item(self, item, spider):
        if not self.is_car_exist(item):
            self.collection.insert_one(item)
            return item
        else:
            if item["price"]["price"][0]['price'] != self.last_price:
                self.collection.update_one({'_id': self._id},
                                           {'$push': {'price.price': item['price']['price'][0]}})
                logger.info(f"Price has changed for car: {item['id']}")
            else:
                logger.info(f"Price has not changed for car: {item['id']}")
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
