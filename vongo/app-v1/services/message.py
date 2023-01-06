import logging
import time

import boto3
from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import MessageConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class MessageService(ExpandableResource):
    def __init__(self, contact_service, user_service) -> None:
        self.collection = mdb[MessageConfig.db][MessageConfig.collection]
        self.expandables = MessageConfig.expandables
        self.Model = MessageConfig.model
        self.object = MessageConfig.object
        self.prefix = MessageConfig.prefix
        self.search_index = MessageConfig.search_index

        # Internal services
        self.contact_service = contact_service
        self.user_service = user_service

        # External services
        self.ses = boto3.client("ses")

    def _send_app_message(self, message: dict) -> str:
        """Send a app message.

        Args:
            message (dict): The message to send.
            contact (dict): The contact to send the message to.

        Returns:
            str: Status of the message.
        """
        logging.info("Sending app message", extra={"message": message})
        return "sent"

    # def _send_email_message(self, body: str, subject: str, from_email: str, to_email: str) -> str:
    #     """Send an email message.

    #     Args:
    #         body (str): The body of the message.
    #         subject (str): The subject of the message.
    #         from_email (str): The email address to send the message from.
    #         to_email (str): The email address to send the message to.

    #     Returns:
    #         str: Status of the message.
    #     """
    #     logging.info('Sending email message')

    #     # TODO: Implement from email
    #     from_email = 'messages@versifylabs.com'

    #     response = self.ses.send_email(
    #         Source=from_email,
    #         Destination={
    #             'ToAddresses': [to_email],
    #         },
    #         Message={
    #             'Subject': {
    #                 'Data': subject,
    #                 'Charset': 'UTF-8',
    #             },
    #             'Body': {
    #                 'Text': {
    #                     'Data': body,
    #                     'Charset': 'UTF-8',
    #                 },
    #             },
    #         },
    #     )
    #     print(response)

    #     return 'pending'

    # def _send_sms_message(self, message: dict, contact: dict) -> str:
    #     """Send an SMS message.

    #     Args:
    #         message (dict): The message to send.
    #         contact (dict): The contact to send the message to.

    #     Returns:
    #         str: Status of the message.
    #     """
    #     logging.info('Sending SMS message', extra={'message': message})
    #     return 'pending'

    def create(self, body: dict) -> dict:
        """Create a new message. If the message already exists, update the message.

        Args:
            body (dict): The message to create.

        Returns:
            dict: The message.
        """
        logging.info("Creating message", extra={"body": body})

        # Create universal fields
        body["_id"] = body.get("_id", f"{self.prefix}_{ObjectId()}")
        body["created"] = int(time.time())
        body["updated"] = int(time.time())

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count messages.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of messages.
        """
        logging.info("Counting messages", extra={"filter": filter})

        # Get messages from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List messages.

        Args:
            query (dict): The query to use.

        Returns:
            list: The messages.
        """
        logging.info("Listing messages", extra={"filter": filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort("_id", -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def get(self, message_id: str) -> dict:
        """Get an message by id.

        Args:
            message_id (str): The id of the message to retrieve.

        Returns:
            dict: The message.
        """
        logging.info("Retrieving message", extra={"id": message_id})

        # Find document matching filter
        message = self.collection.find_one(filter={"_id": message_id})
        if not message:
            raise NotFoundError

        # Convert to JSON
        message = self.Model(**message).to_json()

        return message

    def update(self, message_id: str, body: dict) -> dict:
        """Update a message.

        Args:
            message_id (str): The id of the message to update.
            body (dict): The fields to update.

        Returns:
            dict: The message.

        Raises:
            NotFoundError: If the message does not exist.
        """
        logging.info("Updating message", extra={"message_id": message_id})

        # Find document matching filter
        message = self.get(message_id)
        if not message:
            raise NotFoundError

        # Update fields
        message = deep_update(message, body)
        message["updated"] = int(time.time())

        # Validate against schema
        validated_message = self.Model(**message)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={"_id": message_id},
            update={"$set": validated_message.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def send(self, message_id: str) -> dict:
        """Send a message.

        Args:
            message_id (str): The id of the message to send.

        Returns:
            dict: The message.
        """
        logging.info("Sending message", extra={"id": message_id})

        # Find document matching filter
        message = self.collection.find_one({"_id": message_id})

        # Check if message exists
        if not message:
            raise NotFoundError(f"{self.object} not found")

        status = "pending"
        if message["type"] == "app":
            status = self._send_app_message(message)
        # elif message['type'] == 'email':
        #     status = self._send_email_message(message)
        # elif message['type'] == 'sms':
        #     status = self._send_sms_message(message)
        else:
            raise ValueError("Invalid message type")

        updated_message = self.update(message_id, {"status": status})

        return updated_message

    def delete(self, message_id: str) -> bool:
        """Delete an message.

        Args:
            message_id (str): The id of the message to delete.

        Returns:
            bool: True if the message was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({"_id": message_id})

        return True if deleted else False
