import time

from aws_lambda_powertools import Logger, Tracer
from bson.objectid import ObjectId

from ..api.errors import BadRequestError, NotFoundError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb

logger = Logger()
tracer = Tracer()


class EventService(ExpandableResource):

    def __init__(self) -> None:
        _config = config['event']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

    def create(self, body: dict) -> dict:
        """Create a new event. If the event already exists, update the event.

        Args:
            body (dict): The event to create.

        Returns:
            dict: The event.
        """
        logger.info('Creating event', extra={'event': body})

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
        """Count events.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of events.
        """
        logger.info('Counting events', extra={'filter': filter})

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
        logger.info('Listing events', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve_by_id(self, event_id: str) -> dict:
        """Get an event by id.

        Args:
            event_id (str): The id of the event to retrieve.

        Returns:
            dict: The event.
        """
        logger.info('Retrieving event', extra={'id': event_id})

        # Find document matching filter
        event = self.collection.find_one(filter={'_id': event_id})
        if not event:
            raise NotFoundError

        # Convert to JSON
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
        if not deleted:
            raise NotFoundError

        return True
