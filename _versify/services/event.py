import logging
import time
from typing import Optional

from bson.objectid import ObjectId

from ..config import EventConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class EventService(ExpandableResource):

    def __init__(self, contact_service) -> None:
        self.collection = mdb[EventConfig.db][EventConfig.collection]
        self.expandables = EventConfig.expandables
        self.Model = EventConfig.model
        self.object = EventConfig.object
        self.prefix = EventConfig.prefix
        self.search_index = EventConfig.search_index

        # Internal services
        self.contact_service = contact_service

    def create(self, body: dict) -> dict:
        """Create a new event.

        Args:
            body (dict): The event to create.

        Returns:
            dict: The event.
        """
        logging.info('Creating event', extra={'event': body})

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Determine contact
        if body.get('contact'):
            self.contact_service.get(body['contact'])
        elif body.get('email'):
            contact_body = {
                'account': body['account'],
                'email': body.pop('email')
            }
            contact = self.contact_service.create(contact_body)
            body['contact'] = contact['id']
        elif body.get('detail', {}).get('email'):
            contact_body = {
                'account': body['account'],
                'email': body['detail']['email']
            }
            contact = self.contact_service.create(contact_body)
            body['contact'] = contact['id']
        else:
            raise ValueError('Missing necessary data to identify contact.')

        # Normalize fields
        body['detail_type'] = body.get('detail_type', 'unknown')
        body['detail_type'] = body['detail_type'].lower().strip()
        body['detail_type'] = body['detail_type'].replace(' ', '.')
        body['detail_type'] = body['detail_type'].replace('-', '.')
        body['detail_type'] = body['detail_type'].replace('..', '.')
        body['detail_type'] = body['detail_type'].replace('$', '.')
        body['source'] = body.get('source', 'unknown')
        body['source'] = body['source'].lower().strip()
        body['source'] = body['source'].replace(' ', '_')
        body['source'] = body['source'].replace('-', '_')
        body['source'] = body['source'].replace('__', '_')

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count events.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of events.
        """
        logging.info('Counting events', extra={'filter': filter})

        # Get events from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List events.

        Args:
            query (dict): The query to use.

        Returns:
            list: The events.
        """
        logging.info('Listing events', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def get(self, event_id: str) -> Optional[dict]:
        """Get an event by id.

        Args:
            event_id (str): The id of the event to retrieve.

        Returns:
            dict: The event.
        """
        logging.info('Retrieving event', extra={'id': event_id})

        # Find document matching filter
        event = self.collection.find_one(filter={'_id': event_id})

        # Convert to JSON
        if event:
            event = self.Model(**event).to_json()

        return event

    def delete(self, event_id: str) -> bool:
        """Delete an event.

        Args:
            event_id (str): The id of the event to delete.

        Returns:
            bool: True if the event was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': event_id
        })

        return True if deleted else False
