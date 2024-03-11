from itemadapter import ItemAdapter
from pymongo import MongoClient
from .settings import BOT_NAME


class OtomotoPipeline:
    def process_item(self, item, spider):
        return item


class OtomotoMongoPipeline:
    def __init__(self):
        client = 'MongoClient("mongodb://localhost:27017")'
        self.db = 'client[BOT_NAME]'

    def process_item(self, item, spider):
        print(item)
        return item
