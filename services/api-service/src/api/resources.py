import os
import time

from aws_lambda_powertools import Logger
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..utils.expand import expand_object
from ..utils.mongo import mdb
from .config import config
from .errors import NotFoundError

logger = Logger()


ENVIRONMENT = os.environ['ENVIRONMENT']
if ENVIRONMENT == 'prod':
    MINT_URL = 'https://mint.versifylabs.com'
else:
    MINT_URL = 'https://mint-dev.versifylabs.com'


class ApiResource:

    def __init__(
        self,
        resource: str,
    ):
        cfg = config[resource]
        self.collection = mdb[cfg.db][cfg.collection]
        self.expandables = cfg.expandables
        self.object = cfg.object
        self.prefix = cfg.prefix or cfg.object
        self.Model = cfg.model
        self.search_index = cfg.search_index

    def count(self, filter: dict) -> int:
        return self.collection.count_documents(filter)

    def enrich(self, data: dict) -> dict:
        return data

    def expand(self, data, expand_list):
        if type(data) == list:
            data = {'data': data, 'object': 'list'}
        for path in expand_list:
            if path.startswith('data'):
                new_data = []
                new_path = path[5:]
                for obj in data['data']:  # type: ignore
                    new_data.append(expand_object(obj, new_path))
                data['data'] = new_data  # type: ignore
            else:
                data = expand_object(data, path)
        return data

    def find(self, filter: dict, limit: int = 20, skip: int = 0) -> list:
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)
        return [self.Model(**doc).to_json() for doc in cursor]

    def create(self, body: dict, expand_list: list = []) -> dict:
        logger.info('Creating object', extra={'body': body})

        # Create universal fields
        body['_id'] = f'{self.prefix}_{ObjectId()}'
        body['created'] = int(time.time())

        # Enrich payload data with object specific fields
        body = self.enrich(body)

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON and expand fields
        data = data.to_json()
        return self.expand(data, expand_list)  # type: ignore

    def delete(self, filter: dict) -> bool:
        logger.info('Deleting object', extra={'filter': filter})

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete(filter)
        if not deleted:
            raise NotFoundError

        return True

    def get(self, filter: dict, expand_list: list = []) -> dict:
        logger.info('Getting object', extra={'filter': filter})

        # Find document matching filter
        data = self.collection.find_one(filter)
        if not data:
            raise NotFoundError

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        return self.expand(data, expand_list)  # type: ignore

    def list(
        self,
        filter: dict = {},
        limit: int = 20,
        skip: int = 0,
        expand_list: list = []
    ) -> list:
        logger.info('Listing objects', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        # Convert to JSON and expand fields
        data = self.expand(data, expand_list)  # type: ignore
        return data.get('data', [])  # type: ignore

    def update(
        self,
        body: dict,
        filter: dict,
        expand_list=[]
    ) -> dict:
        logger.info('Updating object', extra={'filter': filter})

        # Get document matching filter
        data = self.get(filter)

        # Update data with payload
        data.update(body)

        # Update document in DB
        data = self.collection.find_one_and_update(
            filter,
            {'$set': self.Model(**data).to_bson()},
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        return self.expand(data, expand_list)  # type: ignore


class Account(ApiResource):

    def __init__(self):
        object = 'account'
        super().__init__(object)


class Airdrop(ApiResource):

    def __init__(self):
        object = 'airdrop'
        super().__init__(object)


class Collection(ApiResource):

    def __init__(self):
        object = 'collection'
        super().__init__(object)

    def create(self, body, expand_list=[]):
        # TODO: Validate against billing usage
        return super().create(body, expand_list)


class Contact(ApiResource):

    def __init__(self):
        object = 'contact'
        super().__init__(object)

    def upsert(self, body, expand_list):
        """Check if email exists. If yes, merge with existing contact"""

        filter = {
            'email': body['email'],
            'organization': body['organization']
        }
        existing_contacts = self.list(filter)
        logger.info(existing_contacts)

        if len(existing_contacts) > 0:
            existing_contact = existing_contacts[0]
            filter['_id'] = existing_contact['id']
            return super().update(body, filter, expand_list)
        else:
            return super().create(body, expand_list)

    def create(self, body, expand_list):
        return self.upsert(body, expand_list)


class Event(ApiResource):

    def __init__(self):
        object = 'event'
        super().__init__(object)


class MintLink(ApiResource):

    def __init__(self):
        object = 'mint_link'
        super().__init__(object)

    def enrich(self, raw):
        raw['url'] = MINT_URL + '/link/' + raw['_id']
        return super().enrich(raw)


class Mint(ApiResource):

    def __init__(self):
        object = 'mint'
        super().__init__(object)

    def enrich(self, raw):
        raw['url'] = MINT_URL + '/mint/' + raw['_id']
        return super().enrich(raw)


class Note(ApiResource):

    def __init__(self):
        object = 'note'
        super().__init__(object)


class Product(ApiResource):

    def __init__(self):
        object = 'product'
        super().__init__(object)


class Signature:

    def __init__(self):
        self.object = 'signature'

    def exists(self, id: str):

        # Add signature id to query
        params = {'signature': id}

        # Check collections
        resource = Collection()
        collections = resource.list(params)

        # Check mints
        resource = Mint()
        mints = resource.list(params)

        if len(collections) + len(mints) > 0:
            return True
        raise NotFoundError


class Webhook(ApiResource):

    def __init__(self):
        object = 'webhook'
        super().__init__(object)
