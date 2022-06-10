import os
import uuid

import pymongo
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers
from versify.utilities.model import response

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

# Fetch mongo env vars
usr = os.environ['MONGO_DB_USER']
pwd = os.environ['MONGO_DB_PASS']
mongo_db_name = os.environ['MONGO_DB_NAME']
mongo_collection_name = os.environ['MONGO_COLLECTION_NAME']
url = os.environ['MONGO_DB_URL']

# Connection String
client = pymongo.MongoClient(
    f"mongodb+srv://{usr}:{pwd}@{url}/?retryWrites=true&w=majority")
db = client.test

try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db = client[mongo_db_name]
collection = db[mongo_collection_name]


@app.post("/poc/v1/events")
@tracer.capture_method
def create_event():
    payload = app.current_event.json_body

    # create item to insert
    document = payload
    document['_id'] = str(uuid.uuid1())
    logger.info({'document': document})

    # write document to database
    collection.insert_one(document)
    logger.info('Inserted document into collection')

    return response('create', document)


@ cors_headers
@ logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@ tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
