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
        self.cluster = MongoClient(connection_str)  # type: ignore
        self.current_user_id = None

    def get_db(self, db_name: str) -> Database:
        return self.cluster[db_name]

    def get_collection(self, db_name: str, collection_name: str) -> Collection:
        return self.cluster[db_name][collection_name]

    def close(self) -> None:
        self.cluster.close()
