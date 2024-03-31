from pymongo import MongoClient
from config import mongo_db


class OtomotoPipeline:
    def process_item(self, item, spider):
        return item


class OtomotoMongoPipeline:
    client = MongoClient(mongo_db.url)
    db = client[mongo_db.db_name]
    collection = db[mongo_db.collection]

    def __init__(self, last_price=None, _id=None):
        self.last_price = last_price
        self._id = _id

    def process_item(self, item, spider):
        spider.logger.info(f"Processing car with id: {item['id']}")
        try:
            car_exist = self.is_car_exist(item)
            if not car_exist:
                self.collection.insert_one(item)
                spider.logger.debug(f"Car added to database: {item['id']}")
                return item
            else:
                if item["price"]["prices"][0]['price'] != self.last_price:
                    self.collection.update_one({'_id': self._id},
                                               {'$push': {'price.prices': item['price']['prices'][0]}})
                    spider.logger.info(f"Price has changed for car: {item['id']}")
                else:
                    spider.logger.debug(f"Price has not changed for car: {item['id']}")
                return item
        except Exception as e:
            spider.logger.error(f"Error {e} while processing car: {item['id']} url {item['url']}")
            return item

    def is_car_exist(self, item):
        car = self.collection.find_one({'id': item['id']})
        if car:
            self._id = car['_id']
        self.last_price = self.get_last_price(car['price']['prices']) if car else None
        return True if car else False

    def get_last_price(self, data):
        sorted_prices = sorted(data, key=lambda x: x['time'], reverse=True)
        return sorted_prices[0]['price']
