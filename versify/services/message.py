import logging
import time

import boto3
from bson.objectid import ObjectId

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
        self.ses = boto3.client('ses')

    def _send_app_message(self, message: dict, contact: dict) -> str:
        """Send a app message.

        Args:
            message (dict): The message to send.
            contact (dict): The contact to send the message to.

        Returns:
            str: Status of the message.
        """
        logging.info('Sending app message', extra={'message': message})
        return 'pending'

    def _send_email_message(self, body: str, subject: str, from_email: str, to_email: str) -> str:
        """Send an email message.

        Args:
            body (str): The body of the message.
            subject (str): The subject of the message.
            from_email (str): The email address to send the message from.
            to_email (str): The email address to send the message to.

        Returns:
            str: Status of the message.
        """
        logging.info('Sending email message')

        # TODO: Implement from email
        from_email = 'messages@versifylabs.com'

        response = self.ses.send_email(
            Source=from_email,
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8',
                },
                'Body': {
                    'Text': {
                        'Data': body,
                        'Charset': 'UTF-8',
                    },
                },
            },
        )
        print(response)

        return 'pending'

    def _send_sms_message(self, message: dict, contact: dict) -> str:
        """Send an SMS message.

        Args:
            message (dict): The message to send.
            contact (dict): The contact to send the message to.

        Returns:
            str: Status of the message.
        """
        logging.info('Sending SMS message', extra={'message': message})
        return 'pending'

    def create(self, body: dict) -> dict:
        """Create a new message. If the message already exists, update the message.

        Args:
            body (dict): The message to create.

        Returns:
            dict: The message.
        """
        logging.info('Creating message', extra={'body': body})

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Get contact and team member objects to send message to and from
        contact_id = body.get('contact')
        contact = self.contact_service.retrieve_by_id(contact_id)
        member_id = body.get('member')
        member = self.user_service.retrieve_by_id(member_id)

        # Check message type
        status = 'pending'
        if body['type'] == 'app':
            status = self._send_app_message(body, contact)
        elif body['type'] == 'email':
            status = self._send_email_message(
                body=body['body'],
                subject=body['subject'],
                from_email=member['email'],
                to_email=contact['email']
            )
        elif body['type'] == 'sms':
            status = self._send_sms_message(body, contact)
        body['status'] = status

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
        logging.info('Counting messages', extra={'filter': filter})

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
        logging.info('Listing messages', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve_by_id(self, message_id: str) -> dict:
        """Get an message by id.

        Args:
            message_id (str): The id of the message to retrieve.

        Returns:
            dict: The message.
        """
        logging.info('Retrieving message', extra={'id': message_id})

        # Find document matching filter
        message = self.collection.find_one(filter={'_id': message_id})
        if not message:
            raise NotFoundError

        # Convert to JSON
        message = self.Model(**message).to_json()

        return message

    def delete(self, message_id: str) -> bool:
        """Delete an message.

        Args:
            message_id (str): The id of the message to delete.

        Returns:
            bool: True if the message was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': message_id
        })
        if not deleted:
            raise NotFoundError

        return True
