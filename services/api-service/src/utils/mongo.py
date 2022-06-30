import os
import pymongo

# Connect to MongoDB Atlas
url = os.environ['MONGO_DB_URL']
connection_str = f"mongodb+srv://{url}/?authSource=$external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority"
mdb = pymongo.MongoClient(connection_str)

try:
    print(mdb.server_info())
except Exception:
    print("Unable to connect to the server.")
