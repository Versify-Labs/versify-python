import logging
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import JourneyRunConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class JourneyRunService(ExpandableResource):

    def __init__(self, contact_service, journey_service, mint_service) -> None:
        self.collection = mdb[JourneyRunConfig.db][JourneyRunConfig.collection]
        self.expandables = JourneyRunConfig.expandables
        self.Model = JourneyRunConfig.model
        self.object = JourneyRunConfig.object
        self.prefix = JourneyRunConfig.prefix
        self.search_index = JourneyRunConfig.search_index

        # Internal services
        self.contact_service = contact_service
        self.mint_service = mint_service
        self.journey_service = journey_service

    def create(self, body: dict) -> dict:
        """Create a new journey_run. If the journey_run already exists, update the journey_run.

        Args:
            body (dict): The journey_run to create.

        Returns:
            dict: The journey_run.
        """
        logging.info('Creating journey_run', extra={'journey_run': body})

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
        """Count journey_runs.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of journey_runs.
        """
        logging.info('Counting journey_runs', extra={'filter': filter})

        # Get journey_runs from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List journey_runs.

        Args:
            query (dict): The query to use.

        Returns:
            list: The journey_runs.
        """
        logging.info('Listing journey_runs', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve_by_id(self, journey_run_id: str) -> dict:
        """Get an journey_run by id.

        Args:
            journey_run_id (str): The id of the journey_run to retrieve.

        Returns:
            dict: The journey_run.
        """
        logging.info('Retrieving journey_run', extra={'id': journey_run_id})

        # Find document matching filter
        journey_run = self.collection.find_one(filter={'_id': journey_run_id})
        if not journey_run:
            raise NotFoundError

        # Convert to JSON
        journey_run = self.Model(**journey_run).to_json()

        return journey_run

    def update(self, id: str, body: dict) -> dict:
        """Update a journey_run.

        Args:
            id (str): The id of the journey_run to update.
            body (dict): The fields to body.

        Returns:
            dict: The journey_run.

        Raises:
            NotFoundError: If the journey_run does not exist.
        """
        logging.info('Updating journey_run', extra={'id': id})

        # Find document matching filter
        journey_run = self.collection.find_one(filter={'_id': id})
        if not journey_run:
            raise NotFoundError

        # Update fields
        journey_run = deep_update(journey_run, body)
        journey_run['updated'] = int(time.time())

        # Validate against schema
        validated_journey_run = self.Model(**journey_run)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': id},
            update={'$set': validated_journey_run.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data
