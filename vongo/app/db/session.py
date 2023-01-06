import logging
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from ..core.config import settings


class SessionLocal:
    def __init__(self) -> None:

        if settings.MONGO_DB_URL:
            # Create connection string for MongoDB Atlas using AWS IAM
            url = settings.MONGO_DB_URL
            connection_str = f"mongodb+srv://{url}/?authSource=$external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority"
        else:
            # Create connection string for MongoDB Atlas using username and password
            mongo_domain = settings.MONGO_DOMAIN
            mongo_user = settings.MONGO_UN
            mongo_password = settings.MONGO_PW
            connection_str = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_domain}/?retryWrites=true&w=majority"

        self._client = None
        try:
            self._client = MongoClient(connection_str)
            print("Connected to MongoDB")
        except Exception as e:
            print(e)
            print("Could not connect to MongoDB")

    @property
    def client(self) -> Optional[MongoClient]:

        if self._client is None:
            logging.error("Database not initialized")
            return None

        return self._client

    def get_db(self, db_name: str) -> Optional[Database]:

        if not self.client:
            return None

        return self.client[db_name]

    def get_collection(
        self, db_name: str, collection_name: str
    ) -> Optional[Collection]:

        if not self.client:
            return None

        if db_name not in self.client.list_database_names():
            return None

        db = self.client[db_name]
        if collection_name not in db.list_collection_names():
            return None

        return db[collection_name]

    def close(self) -> None:
        self.client.close()
