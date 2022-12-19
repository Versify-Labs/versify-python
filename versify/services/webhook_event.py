import logging
import time

from bson.objectid import ObjectId

from ..config import WebhookEventConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class WebhookEventService(ExpandableResource):

    def __init__(self) -> None:
        self.collection = mdb[WebhookEventConfig.db][WebhookEventConfig.collection]
        self.expandables = WebhookEventConfig.expandables
        self.Model = WebhookEventConfig.model
        self.object = WebhookEventConfig.object
        self.prefix = WebhookEventConfig.prefix
        self.search_index = WebhookEventConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new webhook_event. If the webhook_event already exists, update the webhook_event.

        Args:
            body (dict): The webhook_event to create.

        Returns:
            dict: The webhook_event.
        """
        logging.info('Creating webhook_event', extra={'webhook_event': body})

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count webhook_events.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of webhook_events.
        """
        logging.info('Counting webhook_events', extra={'filter': filter})

        # Get webhook_events from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List webhook_events.

        Args:
            query (dict): The query to use.

        Returns:
            list: The webhook_events.
        """
        logging.info('Listing webhook_events', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve_by_id(self, webhook_event_id: str) -> dict:
        """Get an webhook_event by id.

        Args:
            webhook_event_id (str): The id of the webhook_event to retrieve.

        Returns:
            dict: The webhook_event.
        """
        logging.info('Retrieving webhook_event',
                     extra={'id': webhook_event_id})

        # Find document matching filter
        webhook_event = self.collection.find_one(
            filter={'_id': webhook_event_id})
        if not webhook_event:
            raise NotFoundError

        # Convert to JSON
        webhook_event = self.Model(**webhook_event).to_json()

        return webhook_event

    def delete(self, webhook_event_id: str) -> bool:
        """Delete an webhook_event.

        Args:
            webhook_event_id (str): The id of the webhook_event to delete.

        Returns:
            bool: True if the webhook_event was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': webhook_event_id
        })
        if not deleted:
            raise NotFoundError

        return True
