import logging
import time
from typing import List

import simplejson as json
from bson.json_util import dumps
from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import ContactConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb
from ..utils.pipelines import match_stage, search_stage, vql_stage


class ContactService(ExpandableResource):

    def __init__(self):
        self.collection = mdb[ContactConfig.db][ContactConfig.collection]
        self.expandables = ContactConfig.expandables
        self.Model = ContactConfig.model
        self.object = ContactConfig.object
        self.prefix = ContactConfig.prefix
        self.search_index = ContactConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new contact. If the contact email already exists, update the contact.

        Args:
            contact (dict): The contact to create.

        Returns:
            dict: The contact.
        """
        logging.info('Creating contact', extra={'body': body})

        # Sanitize body
        body['email'] = body['email'].lower()

        # Check if email already exists
        contacts = self.list(
            filter={
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
        logging.info('Counting contacts', extra={'filter': filter})

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
        logging.info('Listing contacts', extra={'filter': filter})

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
        logging.info('Retrieving contact', extra={'id': contact_id})

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
        logging.info('Updating contact', extra={'contact_id': contact_id})

        # Find document matching filter
        contact = self.collection.find_one(filter={'_id': contact_id})
        if not contact:
            raise NotFoundError

        # Update fields
        contact = deep_update(contact, body)
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
        logging.info('Searching contacts', extra={'query': query})

        # Find documents matching filter
        cursor = self.collection.aggregate([
            search_stage(index=self.search_index, query=query),
            match_stage(account=account_id),
        ])

        # Convert cursor to list
        contacts = [self.Model(**doc).to_json() for doc in cursor]

        return contacts

    def aggregate_tags(self, account_id):
        stages = [
            match_stage(account=account_id),
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
        data = list(cursor)
        data = dumps(data)
        data = json.loads(data)
        tags = []
        if data and len(data) > 0:
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
            vql_stage(account=account_id, vql=vql),
        ]
        logging.info(stages)
        cursor = self.collection.aggregate(stages)
        return [self.Model(**doc).to_json() for doc in cursor]

    def bulk_update(self, ids: List = [], body: dict = {}):
        """Bulk update contacts.

        Args:
            ids (List): The ids of the contacts to update.
            body (dict): The fields to update.

        Returns:
            dict: The contact.
        """
        logging.info('Bulk updating contacts', extra={'ids': ids})

        # Update fields
        body['updated'] = int(time.time())

        # Update items in DB
        data = self.collection.update_many(
            filter={'_id': {'$in': ids}},
            update={'$set': body},
        )
        return data.modified_count

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
