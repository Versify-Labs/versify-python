import logging
import os
import time
from typing import Optional

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import CollectionConfig
from ..utils.exceptions import NotFoundError, UsageLimitError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb
from ..utils.tatum import Tatum

if os.environ.get('ENVIRONMENT', 'dev') == 'prod':
    METADATA_URI_BASE = "https://cdn.versifylabs.com"
else:
    METADATA_URI_BASE = "https://cdn-dev.versifylabs.com"


class CollectionService(ExpandableResource):

    def __init__(self) -> None:
        self.collection = mdb[CollectionConfig.db][CollectionConfig.collection]
        self.expandables = CollectionConfig.expandables
        self.Model = CollectionConfig.model
        self.object = CollectionConfig.object
        self.prefix = CollectionConfig.prefix
        self.search_index = CollectionConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new account. If the account already exists, update the account.

        Args:
            account (dict): The account to create.

        Returns:
            dict: The account.
        """
        logging.info('Creating collection', extra={'body': body})

        # Create fields
        collection_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = collection_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # TODO: Validate against billing usage
        within_usage_limit = True
        if not within_usage_limit:
            raise UsageLimitError

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        # Return collection after contract is deployed
        self.deploy(collection_id)

        return data

    def count(self, filter: dict) -> int:
        """Count collections.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of collections.
        """
        logging.info('Counting collections', extra={'filter': filter})

        # Get collections from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List collections.

        Args:
            query (dict): The query to use.

        Returns:
            list: The collections.
        """
        logging.info('Listing collections', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve(
        self,
        collection_id: Optional[str] = None,
        account_id: Optional[str] = None,
        default: Optional[bool] = None,
    ) -> dict:
        logging.info('Retrieving collection')

        # Construct filter
        filter = {}
        if account_id:
            filter['account'] = account_id
        if collection_id:
            filter['_id'] = collection_id
        if default:
            filter['default'] = True

        # Find document matching filter
        collection = self.collection.find_one(filter=filter)
        if not collection:
            raise NotFoundError

        # Convert to JSON
        collection = self.Model(**collection).to_json()

        return collection

    def update(self, collection_id: str, body: dict) -> dict:
        """Update a collection. If the collection does not exist, create a new collection.

        Args:
            collection_id (str): The id of the collection to update.
            body (dict): The fields to update.

        Returns:
            dict: The collection.

        Raises:
            NotFoundError: If the collection does not exist.
        """
        logging.info('Updating collection', extra={'id': collection_id})

        # Find document matching filter
        collection = self.collection.find_one(filter={'_id': collection_id})
        if not collection:
            raise NotFoundError

        # Update fields
        collection = deep_update(collection, body)
        collection['updated'] = int(time.time())

        # Validate against schema
        validated_collection = self.Model(**collection)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': collection_id},
            update={'$set': validated_collection.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def deploy(self, collection_id: str) -> dict:
        """Deploy ERC1155 smart contract for the collection

        Args:
            collection_id (str): ID of the collection

        Returns:
            collection (dict): Updated collection
        """

        # Deploy ERC1155 smart contract for the collection
        tatum = Tatum()
        token_uri = f"{METADATA_URI_BASE}/products/{collection_id}" + "/{id}.json"
        response = tatum.deploy_contract(token_uri)
        signature = response.get('signatureId')

        # Update collection in DB with txn result
        update_body = {
            'uri': token_uri,
            'signature': signature,
            'status': 'pending' if signature else 'failed'
        }
        data = self.collection.find_one_and_update(
            filter={'_id': collection_id},
            update={'$set': update_body},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, collection_id: str) -> bool:
        """Delete an collection.

        Args:
            collection_id (str): The id of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': collection_id
        })
        if not deleted:
            raise NotFoundError

        return True
