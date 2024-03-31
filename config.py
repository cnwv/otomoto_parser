import os


class MongoConfig:
    def __init__(self):
        self.MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        self.MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        self.db_name = os.getenv("DB")
        self.collection = os.getenv("COLLECTION")
        self.host = os.getenv("HOST")
        self.url = f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.host}:27017"


mongo_db = MongoConfig()
