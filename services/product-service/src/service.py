import json
import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.utilities import parameters
from pynamodb.exceptions import DoesNotExist
from versify.utilities.model import generate_uuid

from .model import CollectionModel, ProductModel

ENV = os.environ['ENVIRONMENT']
METADATA_BUCKET = f"cdn{'-dev' if ENV == 'dev' else ''}.versifylabs.com"
METADATA_URI_BASE = f"https://cdn{'-dev' if ENV == 'dev' else ''}.versifylabs.com"
SECRET_NAME = os.environ['SECRET_NAME']
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
    my_bucket = s3_resource.Bucket(METADATA_BUCKET)
    max_token_id = 0
    for obj in my_bucket.objects.filter(Prefix=f"products/{collection_id}/"):
        key_parts = obj.key.split('/')
        fname = key_parts[-1]
        if not fname.startswith('0x') and fname.endswith('.json'):
            token_id = int(fname.split('.')[0])
            max_token_id = max(max_token_id, token_id)
    return max_token_id


def move_s3_object(old_key, new_key):
    my_bucket = METADATA_BUCKET
    current_object_key = old_key
    new_object_key = new_key
    copy_source = {
        'Bucket':  my_bucket,
        'Key': current_object_key
    }
    s3_resource.meta.client.copy(copy_source, my_bucket, new_object_key)
    return True


def upload_metadata_to_s3(key, metadata):
    return s3_client.put_object(
        Body=json.dumps(metadata),
        Bucket=METADATA_BUCKET,
        Key=key
    )


class Collections:

    def __init__(self, organization: str):
        self.model = CollectionModel
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new collection"""
        id = generate_uuid('collection')
        body['PK'] = id
        body['SK'] = id
        body['id'] = id
        body['organization'] = self.organization
        body['token_uri'] = get_contract_token_uri(id)
        collection = self.model(**body)
        collection.save()
        return collection.to_dict() if raw else collection

    def list(self, query: dict = {}, raw: bool = True):
        """Retrieves an collection by its id"""
        collections = self.model.by_organization_by_object.query(
            hash_key=self.organization,
            range_key_condition=self.model.object == 'collection'
        )
        return self.to_list(collections) if raw else collections

    def get(self, id: str, raw: bool = True):
        """Retrieves an collection by its id"""
        try:
            item = self.model.get(id, id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing collection"""
        collection = self.get(id, raw=False)
        actions = []
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        collection.update(actions=actions)
        return collection.to_dict() if raw else collection

    def update_collection_with_contract(self, id: str, contract: str, raw: bool = True):
        collection = self.get(id, raw=False)
        address = contract
        actions = [
            self.model.address.set(address),
            self.model.state.set('deployed')
        ]
        collection.update(actions=actions)
        return collection.to_dict() if raw else collection


class Products:

    def __init__(self, organization: str):
        self.model = ProductModel
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def to_hex(self, x):
        padding = 4
        return f"{x:#0{padding}x}"

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new product"""
        collection_id = body['collection']
        product_id = generate_uuid('product')

        # Get collection from db (we need data from it like contract_adddress)
        collections = Collections(self.organization)
        collection = collections.get(collection_id)
        logger.info(collection)

        if not collection.get('address'):
            err = 'Collection is still pending'
            logger.error(err)
            raise BadRequestError(err)

        # Get Token ID from s3 (in hex)
        max_token_id_dec = get_max_token_id(collection_id)
        token_id_dec = max_token_id_dec + 1
        token_id_hex = self.to_hex(token_id_dec)
        logger.info({
            'contract_address': collection.get('address'),
            'token_id_dec': token_id_dec,
            'token_id_hex': token_id_hex
        })

        # Move product image from /tmp to /metadata/collection_id/token_id
        old_key = '/'.join(body['image'].split('/')[-2:])
        metadata_key_dec = get_metadata_key(collection_id, token_id_dec)
        metadata_key_hex = get_metadata_key(collection_id, token_id_hex)
        image_key = get_image_key(collection_id, token_id_hex)
        image_url = get_image_url(collection_id, token_id_hex)
        move_s3_object(old_key, image_key)

        # Upload product metadata to S3
        metadata = {
            'name': body['name'],
            'description': body['description'],
            'image': image_url,
            "attributes": [
                {
                    "trait_type": "Organization",
                    "value": self.organization
                }
            ],
            'external_url': 'https://versifylabs.com',
            # 'animation_url': '',
            # 'youtube_url': ''
        }
        upload_metadata_to_s3(metadata_key_dec, metadata)
        upload_metadata_to_s3(metadata_key_hex, metadata)

        # Save product to DB
        body['PK'] = product_id
        body['SK'] = product_id
        body['id'] = product_id
        body['collection_details'] = collection
        body['contract_address'] = collection.get('address')
        body['token_id'] = str(token_id_dec)
        body['organization'] = self.organization
        product = self.model(**body)
        product.save()
        return product.to_dict() if raw else product

    def list(self, query: dict = {}, raw: bool = True):
        """Retrieves an product by its id"""
        products = self.model.by_organization_by_object.query(
            hash_key=self.organization,
            range_key_condition=self.model.object == 'product'
        )
        return self.to_list(products) if raw else products

    def get(self, id: str, raw: bool = True):
        """Retrieves an product by its id"""
        try:
            item = self.model.get(id, id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing product"""
        product = self.get(id, raw=False)
        actions = []
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        product.update(actions=actions)
        return product.to_dict() if raw else product

    def update_with_order(self, order: dict):
        """Update products that are included in the order"""
        for item in order['items']:
            product_id = item['product']
            quantity = item['quantity']
            product = self.get(product_id, raw=False)
            product.update(actions=[
                self.model.total_sold.set(product.total_sold + quantity)
            ])
        return True


class Versify:

    def __init__(self, organization: str) -> None:
        self.collections = Collections(organization)
        self.products = Products(organization)
