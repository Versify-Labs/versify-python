import json
import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities import parameters

ENV = os.environ["ENVIRONMENT"]
if ENV == "prod":
    METADATA_BUCKET = "cdn.versifylabs.com"
    METADATA_URI_BASE = "https://cdn.versifylabs.com"
else:
    METADATA_BUCKET = "cdn-dev.versifylabs.com"
    METADATA_URI_BASE = "https://cdn-dev.versifylabs.com"
SECRET_NAME = os.environ["SECRET_NAME"]
SECRET = json.loads(parameters.get_secret(SECRET_NAME))

logger = Logger()
s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")


def get_contract_token_uri(collection_id):
    return f"{METADATA_URI_BASE}/products/{collection_id}" + "/{id}.json"


def get_metadata_key(collection_id, token_id):
    return f"products/{collection_id}/{str(token_id)}.json"


def get_image_key(collection_id, token_id_hex):
    return f"products/{collection_id}/{token_id_hex}.png"


def get_image_url(collection_id, token_id_hex):
    return f"{METADATA_URI_BASE}/products/{collection_id}/{token_id_hex}.png"


def get_max_token_id(collection_id):
    logger.info("Determining greatest token id")
    my_bucket = s3_resource.Bucket(METADATA_BUCKET)
    max_token_id = 0
    for obj in my_bucket.objects.filter(Prefix=f"products/{collection_id}/"):
        key_parts = obj.key.split("/")
        fname = key_parts[-1]
        if not fname.startswith("0x") and fname.endswith(".json"):
            token_id = int(fname.split(".")[0])
            max_token_id = max(max_token_id, token_id)
    return max_token_id


def move_s3_object(old_key, new_key):
    logger.info(f"Moving s3 object {old_key} to {new_key}")
    my_bucket = METADATA_BUCKET
    current_object_key = old_key
    new_object_key = new_key
    copy_source = {"Bucket": my_bucket, "Key": current_object_key}
    s3_resource.meta.client.copy(copy_source, my_bucket, new_object_key)
    return True


def upload_metadata_to_s3(key, metadata):
    logger.info(f"Uploading metadata {key}")
    return s3_client.put_object(
        Body=json.dumps(metadata), Bucket=METADATA_BUCKET, Key=key
    )
