import time

import simplejson as json
from aws_lambda_powertools import Logger, Tracer
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import NotFoundError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb
from ..utils.pipelines import vql_stage

logger = Logger()
tracer = Tracer()


class ContactService(ExpandableResource):

    def __init__(self):
        _config = config['contact']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

    def create(self, body: dict) -> dict:
        """Create a new contact. If the contact email already exists, update the contact.

        Args:
            contact (dict): The contact to create.

        Returns:
            dict: The contact.
        """
        logger.info('Creating contact', extra={'body': body})

        # Check if email already exists
        contacts = self.list(
            {
                'account': body['account'],
                'email': body['email']
            }
        )
        if len(contacts) > 0:
            contact = contacts[0]
            return self.update(contact['id'], body)

        # Create fields
        contact_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = contact_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Validate against schema
        contact = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(contact.to_bson())

        # Convert to JSON
        contact = contact.to_json()

        return contact

    def count(self, filter: dict) -> int:
        """Count contacts.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of contacts.
        """
        logger.info('Counting contacts', extra={'filter': filter})

        # Get contacts from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List contacts.

        Args:
            query (dict): The query to use.

        Returns:
            list: The contacts.
        """
        logger.info('Listing contacts', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        contacts = [self.Model(**doc).to_json() for doc in cursor]

        return contacts

    def retrieve_by_id(self, contact_id: str) -> dict:
        """Get an contact by id.

        Args:
            contact_id (str): The id of the contact to retrieve.

        Returns:
            dict: The contact.
        """
        logger.info('Retrieving contact', extra={'id': contact_id})

        # Find document matching filter
        contact = self.collection.find_one(filter={'_id': contact_id})
        if not contact:
            raise NotFoundError

        # Convert to JSON
        contact = self.Model(**contact).to_json()

        return contact

    def update(self, contact_id: str, body: dict) -> dict:
        """Update a contact. If the contact does not exist, create a new contact.

        Args:
            contact_id (str): The id of the contact to update.
            body (dict): The fields to update.

        Returns:
            dict: The contact.

        Raises:
            NotFoundError: If the contact does not exist.
        """
        logger.info('Updating contact', extra={'contact_id': contact_id})

        # Find document matching filter
        contact = self.collection.find_one(filter={'_id': contact_id})
        if not contact:
            raise NotFoundError

        # Update fields
        contact = {**contact, **body}
        contact['updated'] = int(time.time())

        # Validate against schema
        validated_contact = self.Model(**contact)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': contact_id},
            update={'$set': validated_contact.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, contact_id: str) -> bool:
        """Delete an contact.

        Args:
            contact_id (str): The id of the contact to delete.

        Returns:
            bool: True if the contact was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': contact_id
        })
        if not deleted:
            raise NotFoundError

        return True

    def search(self, account_id, query):
        """Search for contacts.

        Args:
            account_id (str): The id of the account to search contacts for.
            query (dict): The query to use.

        Returns:
            list: The contacts.
        """
        logger.info('Searching contacts', extra={'query': query})

        # Construct filter
        filter = {}
        if account_id:
            filter['account'] = account_id
        if query:
            filter['$text'] = {'$search': query}

        # Find documents matching filter
        cursor = self.collection.find(filter=filter)

        # Convert cursor to list
        contacts = [self.Model(**doc).to_json() for doc in cursor]

        return contacts

    def aggregate_tags(self, account_id):
        stages = [
            {
                "$match": {
                    'account': account_id
                }
            },
            {
                '$unwind': {
                    'path': '$tags',
                    'preserveNullAndEmptyArrays': False
                }
            },
            {
                '$group': {
                    '_id': None,
                    'tags': {
                        '$addToSet': '$tags'
                    }
                }
            }
        ]
        cursor = self.collection.aggregate(stages)
        data = json.loads(dumps(list(cursor)))
        tags = []
        if len(data) > 0:
            tags = sorted(data[0]['tags'])
        return tags

    def count_segment_contacts(self, account_id, vql):
        stages = [
            vql_stage(vql=vql, account=account_id),
            {'$count': "count"}
        ]
        cursor = self.collection.aggregate(stages)
        result = json.loads(dumps(list(cursor)))
        if not result or len(result) < 1:
            return 0
        return result[0]['count']

    def list_segment_contacts(self, account_id, vql):
        stages = [
            vql_stage(vql=vql, account=account_id),
        ]
        cursor = self.collection.aggregate(stages)
        return [self.Model(**doc).to_json() for doc in cursor]

    # def _v2_search(self, account: str, query: dict = {}):
    #     # body = {
    #     #     "query":  {
    #     #         "operator": "AND",
    #     #         "value": [
    #     #             {
    #     #                 "field": "custom_attributes.social_network",
    #     #                 "operator": "=",
    #     #                 "value": "facebook"
    #     #             },
    #     #             {
    #     #                 "field": "custom_attributes.social_network",
    #     #                 "operator": "=",
    #     #                 "value": "twitter"
    #     #             },
    #     #             {
    #     #                 "field": "custom_attributes.social_network",
    #     #                 "operator": "=",
    #     #                 "value": "instagram"
    #     #             }
    #     #         ]
    #     #     }
    #     # }
    #     q = {'account': account}

    #     if query['operator'] == 'AND':
    #         for clause in query['value']:
    #             field = clause['field']
    #             operator = clause['operator']
    #             value = clause['value']
    #             if operator == '=':
    #                 q[field] = value
    #             elif operator == '~':
    #                 q[field] = {'$regex': value}
    #             elif operator == '<':
    #                 q[field] = {'$lt': int(value)}
    #             elif operator == '>':
    #                 q[field] = {'$gt': int(value)}

    #     stages = [{"$match": q}]
    #     cursor = self.collection.aggregate(stages)
    #     return [self.Model(**doc).to_json() for doc in cursor]
