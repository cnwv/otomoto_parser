import os


class MongoConfig:
    def __init__(self):
        self.MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        self.MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        self.url = f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@mongo:27017"
        self.db_name = os.getenv("DB")
        self.collection = os.getenv("COLLECTION")

    def get_url(self):
        return self.url
