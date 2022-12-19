import logging
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import RedemptionConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class RedemptionService(ExpandableResource):

    def __init__(self, contact_service, reward_service) -> None:
        self.collection = mdb[RedemptionConfig.db][RedemptionConfig.collection]
        self.expandables = RedemptionConfig.expandables
        self.Model = RedemptionConfig.model
        self.object = RedemptionConfig.object
        self.prefix = RedemptionConfig.prefix
        self.search_index = RedemptionConfig.search_index

        # Internal services
        self.contact_service = contact_service
        self.reward_service = reward_service

    def create(self, body: dict) -> dict:
        """Create a new redemption. If the redemption already exists, update the redemption.

        Args:
            redemption (dict): The redemption to create.

        Returns:
            dict: The redemption.
        """
        logging.info('Creating redemption', extra={'body': body})

        # Create fields
        redemption_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = redemption_id
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
        """Count redemptions.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of redemptions.
        """
        logging.info('Counting redemptions', extra={'filter': filter})

        # Get redemptions from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List redemptions.

        Args:
            query (dict): The query to use.

        Returns:
            list: The redemptions.
        """
        logging.info('Listing redemptions', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        redemptions = [self.Model(**doc).to_json() for doc in cursor]

        return redemptions

    def get(self, redemption_id: str) -> dict:
        """Get an redemption by id.

        Args:
            redemption_id (str): The id of the redemption to retrieve.

        Returns:
            dict: The redemption.
        """
        logging.info('Retrieving redemption', extra={
                     'redemption_id': redemption_id})

        # Find document matching filter
        redemption = self.collection.find_one(filter={'_id': redemption_id})
        if not redemption:
            raise NotFoundError

        # Convert to JSON
        redemption = self.Model(**redemption).to_json()

        return redemption

    def update(self, redemption_id: str, body: dict) -> dict:
        """Update a redemption. If the redemption does not exist, create a new redemption.

        Args:
            redemption_id (str): The id of the redemption to update.
            body (dict): The fields to update.

        Returns:
            dict: The redemption.

        Raises:
            NotFoundError: If the redemption does not exist.
        """
        logging.info('Updating redemption', extra={
                     'redemption_id': redemption_id})

        # Find document matching filter
        redemption = self.collection.find_one(filter={'_id': redemption_id})
        if not redemption:
            raise NotFoundError

        # Update fields
        redemption = deep_update(redemption, body)
        redemption['updated'] = int(time.time())

        # Validate against schema
        validated_redemption = self.Model(**redemption)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': redemption_id},
            update={'$set': validated_redemption.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, redemption_id: str) -> bool:
        """Delete an redemption.

        Args:
            redemption_id (str): The id of the redemption to delete.

        Returns:
            bool: True if the redemption was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': redemption_id
        })
        if not deleted:
            raise NotFoundError

        return True
