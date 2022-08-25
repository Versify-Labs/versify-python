import time

from aws_lambda_powertools import Logger, Tracer
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import BadRequestError, NotFoundError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb
from ..utils.s3 import (get_image_key, get_image_url, get_max_token_id,
                        get_metadata_key, move_s3_object,
                        upload_metadata_to_s3)

logger = Logger()
tracer = Tracer()


class ProductService(ExpandableResource):

    def __init__(self, collection_service):
        _config = config['product']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

        # Internal services
        self.collection_service = collection_service

    def to_hex(self, x):
        x = int(x)
        padding = 4
        return f"{x:#0{padding}x}"

    def upsert_metadata(self, product):

        # Check product data to see what we need to do
        collection_id = product['collection']
        contract_address = product['contract_address']
        token_id = product.get('token_id')

        # Create token_id if it doesn't exist
        if not token_id:
            max_token_id = get_max_token_id(collection_id)
            token_id = max_token_id + 1
        product['token_id'] = token_id
        token_id_hex = self.to_hex(token_id)

        # Move product image from /tmp to /metadata/collection_id/token_id
        old_key = '/'.join(product['image'].split('/')[-2:])
        metadata_key_dec = get_metadata_key(collection_id, token_id)
        metadata_key_hex = get_metadata_key(collection_id, token_id_hex)
        image_key = get_image_key(collection_id, token_id_hex)
        image_url = get_image_url(collection_id, token_id_hex)
        move_s3_object(old_key, image_key)

        # Upload metadata
        metadata = {
            'name': product['name'],
            'description': product['description'],
            'image': image_url,
            "attributes": product.get('properties', []),
            'external_url': f'https://versifylabs.com/assets/{contract_address}/{token_id}',
            # 'animation_url': '',
            # 'youtube_url': ''
        }
        upload_metadata_to_s3(metadata_key_dec, metadata)
        upload_metadata_to_s3(metadata_key_hex, metadata)

        return product

    def create(self, body: dict) -> dict:
        """Create a new product. If the product email already exists, update the product.

        Args:
            product (dict): The product to create.

        Returns:
            dict: The product.
        """
        logger.info('Creating product', extra={'body': body})

        # Create fields
        product_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = product_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Get collection specifed or accounts default
        account_id = body['account']
        collection_id = body.get('collection')
        collection = self.collection_service.retrieve(
            collection_id=collection_id,
            account_id=account_id,
            default=None if collection_id else True
        )

        # Validate that the collection has been deployed
        if not collection or collection.get('status', 'pending') != 'deployed':
            raise BadRequestError('Collection must be deployed.')

        body['collection'] = collection['id']
        body['chain'] = collection.get('chain', 'polygon')
        body['contract_address'] = collection['contract_address']

        # Upload metadata to S3
        body = self.upsert_metadata(product=body)

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count products.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of products.
        """
        logger.info('Counting products', extra={'filter': filter})

        # Get products from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List products.

        Args:
            filter (dict): The filter to use.

        Returns:
            list: The products.
        """
        logger.info('Listing products', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        products = [self.Model(**doc).to_json() for doc in cursor]

        return products

    def retrieve_by_id(self, product_id: str) -> dict:
        """Get an product by id.

        Args:
            product_id (str): The id of the product to retrieve.

        Returns:
            dict: The product.
        """
        logger.info('Retrieving product', extra={'id': product_id})

        # Find document matching filter
        product = self.collection.find_one(filter={'_id': product_id})
        if not product:
            raise NotFoundError

        # Convert to JSON
        product = self.Model(**product).to_json()

        return product

    def update(self, product_id: str, body: dict) -> dict:
        """Update a product. If the product does not exist, create a new product.

        Args:
            product_id (str): The id of the product to update.
            body (dict): The fields to update.

        Returns:
            dict: The product.

        Raises:
            NotFoundError: If the product does not exist.
        """
        logger.info('Updating product', extra={'product_id': product_id})

        # Find document matching filter
        product = self.collection.find_one(filter={'_id': product_id})
        if not product:
            raise NotFoundError

        # Update fields
        product = {**product, **body}
        product['updated'] = int(time.time())

        # Validate against schema
        validated_product = self.Model(**product)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': product_id},
            update={'$set': validated_product.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        # Upload metadata storage
        self.upsert_metadata(product=data)

        return data

    def delete(self, product_id: str) -> bool:
        """Delete an product.

        Args:
            product_id (str): The id of the product to delete.

        Returns:
            bool: True if the product was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': product_id
        })
        if not deleted:
            raise NotFoundError

        return True

    def search(self, account_id, query):
        """Search for products.

        Args:
            account_id (str): The id of the account to search products for.
            query (dict): The query to use.

        Returns:
            list: The products.
        """
        logger.info('Searching products', extra={'query': query})

        # Construct filter
        filter = {}
        if account_id:
            filter['account'] = account_id
        if query:
            filter['$text'] = {'$search': query}

        # Find documents matching filter
        cursor = self.collection.find(filter=filter)

        # Convert cursor to list
        products = [self.Model(**doc).to_json() for doc in cursor]

        return products
