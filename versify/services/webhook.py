import logging
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import WebhookConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class WebhookService(ExpandableResource):

    def __init__(self) -> None:
        self.collection = mdb[WebhookConfig.db][WebhookConfig.collection]
        self.expandables = WebhookConfig.expandables
        self.Model = WebhookConfig.model
        self.object = WebhookConfig.object
        self.prefix = WebhookConfig.prefix
        self.search_index = WebhookConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new webhook. If the webhook already exists, update the webhook.

        Args:
            webhook (dict): The webhook to create.

        Returns:
            dict: The webhook.
        """
        logging.info('Creating webhook', extra={'webhook': body})

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
        """Count webhooks.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of webhooks.
        """
        logging.info('Counting webhooks', extra={'filter': filter})

        # Get webhooks from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List webhooks.

        Args:
            query (dict): The query to use.

        Returns:
            list: The webhooks.
        """
        logging.info('Listing webhooks', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve_by_id(self, webhook_id: str) -> dict:
        """Get an webhook by id.

        Args:
            webhook_id (str): The id of the webhook to retrieve.

        Returns:
            dict: The webhook.
        """
        logging.info('Retrieving webhook', extra={'id': webhook_id})

        # Find document matching filter
        webhook = self.collection.find_one(filter={'_id': webhook_id})
        if not webhook:
            raise NotFoundError

        # Convert to JSON
        webhook = self.Model(**webhook).to_json()

        return webhook

    def update(self, webhook_id: str, body: dict) -> dict:
        """Update a webhook. If the webhook does not exist, create a new webhook.

        Args:
            webhook_id (str): The id of the webhook to update.
            body (dict): The fields to update.

        Returns:
            dict: The webhook.

        Raises:
            NotFoundError: If the webhook does not exist.
        """
        logging.info('Updating webhook', extra={'webhook_id': webhook_id})

        # Find document matching filter
        webhook = self.collection.find_one(filter={'_id': webhook_id})
        if not webhook:
            raise NotFoundError

        # Update fields
        webhook = deep_update(webhook, body)
        webhook['updated'] = int(time.time())

        # Validate against schema
        validated_webhook = self.Model(**webhook)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': webhook_id},
            update={'$set': validated_webhook.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, webhook_id: str) -> bool:
        """Delete an webhook.

        Args:
            webhook_id (str): The id of the webhook to delete.

        Returns:
            bool: True if the webhook was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': webhook_id
        })
        if not deleted:
            raise NotFoundError

        return True
