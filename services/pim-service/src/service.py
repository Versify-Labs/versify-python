import json
import os
import time

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

    def get_filter_condition(self, options):

        # Handle View
        view_condition = None
        view = options.get('view', 'all')
        if view == 'available':
            view_condition = self.model.active == True
        elif view == 'archived':
            view_condition = self.model.active == False
        else:
            view_condition = self.model.active == True
            view_condition |= self.model.active == False
        condition = view_condition

        # Handle Query
        query_condition = None
        query_attrs = ['name']
        query = options.get('query', '')
        for attr in query_attrs:
            if query_condition != None:
                query_condition |= getattr(self.model, attr).contains(query)
            else:
                query_condition = getattr(self.model, attr).contains(query)
        if query_condition != None:
            condition &= query_condition

        # Handle Filter
        filters_condition = None
        filters = options.get('filters', '').split(',')
        filters = [f for f in filters if f.count('-') == 2]
        for f in filters:
            prop, op, val = f.split('-')
            f_condition = None
            if op == 'equal':
                f_condition = getattr(self.model, prop) == val
            elif op == 'notEqual':
                f_condition = getattr(self.model, prop) != val
            elif op == 'contains':
                f_condition = getattr(self.model, prop).contains(val)
            elif op == 'notContains':
                f_condition = ~getattr(self.model, prop).contains(val)
            elif op == 'startsWith':
                f_condition = getattr(self.model, prop).startswith(val)
            elif op == 'greaterThan':
                f_condition = getattr(self.model, prop) > val
            elif op == 'lessThan':
                f_condition = getattr(self.model, prop) < val
            elif op == 'isBlank':
                f_condition = getattr(self.model, prop).does_not_exist()
            elif op == 'isPresent':
                f_condition = getattr(self.model, prop).exists()
            if f_condition != None:
                if filters_condition != None:
                    filters_condition |= f_condition
                else:
                    filters_condition = f_condition
        if filters_condition != None:
            condition &= filters_condition

        logger.info(condition)
        return condition

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new collection"""
        collection_id = generate_uuid('collection')
        timestamp = int(time.time())
        body['PK'] = f'{self.organization}:collection'
        body['id'] = collection_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['organization'] = self.organization
        body['contract_details'] = {
            'state': 'pending',
            'token_uri': get_contract_token_uri(collection_id)
        }
        collection = self.model(**body)
        collection.save()
        return collection.to_dict() if raw else collection

    def list(self, query_params: dict = {}, raw: bool = True):
        """Retrieves a list of collections for the org"""
        filter_condition = self.get_filter_condition(query_params)
        limit = query_params.get('limit', 20)
        before = int(query_params.get(
            'starting_before', 10000000000000000000)) - 1
        after = int(query_params.get('starting_after', 0)) + 1
        collections = self.model.by_organization.query(
            hash_key=f'{self.organization}:collection',
            range_key_condition=self.model.date_created.between(after, before),
            filter_condition=filter_condition,
            limit=limit,
            scan_index_forward=False
        )
        return self.to_list(collections) if raw else collections

    def get(self, id: str, raw: bool = True):
        """Retrieves a collection by its id"""
        try:
            item = self.model.get(f'{self.organization}:collection', id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing collection"""
        collection = self.get(id, raw=False)
        actions = [self.model.date_updated.set(int(time.time()))]
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        collection.update(actions=actions)
        return collection.to_dict() if raw else collection

    def archive(self, collection_id: str):
        """Archive a collection"""
        body = {'active': False}
        collection = self.update(collection_id, body)
        return collection

    def unarchive(self, collection_id: str):
        """Unarchives a collection and moves it to active"""
        body = {'active': True}
        collection = self.update(collection_id, body)
        return collection

    def update_with_contract(self, id: str, contract: str, raw: bool = True):
        collection = self.get(id, raw=False)
        contract_details = collection.contract_details
        contract_details['address'] = contract
        contract_details['state'] = 'deployed'
        body = {'contract': contract, 'contract_details': contract_details}
        collection = self.update(id, body, raw=False)
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

    def get_filter_condition(self, options):

        # Handle View
        view_condition = None
        view = options.get('view', 'all')
        if view == 'available':
            view_condition = self.model.active == True
        elif view == 'archived':
            view_condition = self.model.active == False
        else:
            view_condition = self.model.active == True
            view_condition |= self.model.active == False
        condition = view_condition

        # Handle Query
        query_condition = None
        query_attrs = ['name', 'description']
        query = options.get('query', '')
        for attr in query_attrs:
            if query_condition != None:
                query_condition |= getattr(self.model, attr).contains(query)
            else:
                query_condition = getattr(self.model, attr).contains(query)
        if query_condition != None:
            condition &= query_condition

        # Handle Filter
        filters_condition = None
        filters = options.get('filters', '').split(',')
        filters = [f for f in filters if f.count('-') == 2]
        for f in filters:
            prop, op, val = f.split('-')
            f_condition = None
            if op == 'equal':
                f_condition = getattr(self.model, prop) == val
            elif op == 'notEqual':
                f_condition = getattr(self.model, prop) != val
            elif op == 'contains':
                f_condition = getattr(self.model, prop).contains(val)
            elif op == 'notContains':
                f_condition = ~getattr(self.model, prop).contains(val)
            elif op == 'startsWith':
                f_condition = getattr(self.model, prop).startswith(val)
            elif op == 'greaterThan':
                f_condition = getattr(self.model, prop) > val
            elif op == 'lessThan':
                f_condition = getattr(self.model, prop) < val
            elif op == 'isBlank':
                f_condition = getattr(self.model, prop).does_not_exist()
            elif op == 'isPresent':
                f_condition = getattr(self.model, prop).exists()
            if f_condition != None:
                if filters_condition != None:
                    filters_condition |= f_condition
                else:
                    filters_condition = f_condition
        if filters_condition != None:
            condition &= filters_condition

        logger.info(condition)
        return condition

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new product"""

        product_id = generate_uuid('product')
        timestamp = int(time.time())
        body['PK'] = f'{self.organization}:product'
        body['id'] = product_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp

        # Get collection from db (we need data from it)
        collection_id = body['collection']
        collections = Collections(self.organization)
        collection = collections.get(collection_id)
        contract_address = collection.get('contract')
        body['collection_details'] = collection

        if not contract_address:
            err = 'Contract is still pending'
            logger.error(err)
            raise BadRequestError(err)

        # Get Token ID from s3 (in hex)
        max_token_id_dec = get_max_token_id(collection_id)
        token_id_dec = max_token_id_dec + 1
        token_id_hex = self.to_hex(token_id_dec)
        logger.info({
            'contract_address': contract_address,
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
            "attributes": body.get('properties', []),
            'external_url': 'https://versifylabs.com',
            # 'animation_url': '',
            # 'youtube_url': ''
        }
        upload_metadata_to_s3(metadata_key_dec, metadata)
        upload_metadata_to_s3(metadata_key_hex, metadata)

        # Save product to DB
        body['token'] = str(token_id_dec)
        body['organization'] = self.organization
        product = self.model(**body)
        product.save()
        return product.to_dict() if raw else product

    def list(self, query_params: dict = {}, raw: bool = True):
        """Retrieves a list of products for the org"""
        filter_condition = self.get_filter_condition(query_params)
        limit = query_params.get('limit', 20)
        before = int(query_params.get(
            'starting_before', 10000000000000000000)) - 1
        after = int(query_params.get('starting_after', 0)) + 1
        products = self.model.by_organization.query(
            hash_key=f'{self.organization}:product',
            range_key_condition=self.model.date_created.between(after, before),
            filter_condition=filter_condition,
            limit=limit,
            scan_index_forward=False
        )
        return self.to_list(products) if raw else products

    def get(self, id: str, raw: bool = True):
        """Retrieves a product by its id"""
        try:
            item = self.model.get(f'{self.organization}:product', id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing product"""
        product = self.get(id, raw=False)
        actions = [self.model.date_updated.set(int(time.time()))]
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        product.update(actions=actions)
        return product.to_dict() if raw else product

    def archive(self, product_id: str):
        """Archive a product"""
        body = {'active': False}
        product = self.update(product_id, body)
        return product

    def unarchive(self, product_id: str):
        """Unarchives a product and moves it to active"""
        body = {'active': True}
        product = self.update(product_id, body)
        return product

    def add_airdrop(self, product_id: str, quantity: int = 1):
        """Add airdrop to a products stats"""
        product = self.get(product_id, raw=False)
        product_dict = product.to_dict()
        total_airdrops = product_dict.get('total_airdrops', 0) + quantity
        body = {'total_airdrops': total_airdrops}
        product = self.update(product_id, body)
        return product.to_dict()

    def update_with_airdrop(self, airdrop: dict):
        """Update product in the airdrop"""
        product_id = airdrop['product']
        product = self.get(product_id, raw=False)
        body = {'total_airdrops': product.total_airdrops + 1}
        self.update(product_id, body)
        return True


class Versify:

    def __init__(self, organization: str) -> None:
        self.collections = Collections(organization)
        self.products = Products(organization)
