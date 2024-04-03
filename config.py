import os


class MongoConfig:
    def __init__(self):
        self.MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        self.MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        self.db_name = os.getenv("DB")
        self.collection = os.getenv("COLLECTION")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.url = f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@" \
                   f"{self.host}:{int(self.port)}"


mongo_db = MongoConfig()
