import time

from aws_lambda_powertools import Logger, Tracer
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import NotFoundError, UsageLimitError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mandrill import mailchimp
from ..utils.mongo import mdb

logger = Logger()
tracer = Tracer()


class AirdropService(ExpandableResource):

    def __init__(
        self,
        account_service,
        contact_service,
        mint_link_service,
        product_service,
    ) -> None:
        _config = config['airdrop']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

        # Internal Services
        self.account_service = account_service
        self.contact_service = contact_service
        self.product_service = product_service
        self.mint_link_service = mint_link_service

    def create(self, body: dict) -> dict:
        """Create a new airdrop. If the airdrop already exists, update the airdrop.

        Args:
            airdrop (dict): The airdrop to create.

        Returns:
            dict: The airdrop.
        """
        logger.info('Creating airdrop', extra={'body': body})

        # Create fields
        airdrop_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = airdrop_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Inject with account fields
        account = self.account_service.retrieve_by_id(body['account'])
        business_profile = account['business_profile']
        business_branding = business_profile['branding']
        body['recipients'] = body.get('recipients') or {}
        body['email_settings']['from_image'] = business_branding.get('logo')
        body['email_settings']['from_name'] = business_profile.get('name')

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List airdrops.

        Args:
            query (dict): The query to use.

        Returns:
            list: The airdrops.
        """
        logger.info('Listing airdrops', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        airdrops = [self.Model(**doc).to_json() for doc in cursor]

        return airdrops

    def count(self, filter: dict) -> int:
        """Count airdrops.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of airdrops.
        """
        logger.info('Counting airdrops', extra={'filter': filter})

        # Get airdrops from DB
        count = self.collection.count_documents(filter)

        return count

    def retrieve_by_id(self, airdrop_id: str) -> dict:
        """Get an airdrop by id.

        Args:
            airdrop_id (str): The id of the airdrop to retrieve.

        Returns:
            dict: The airdrop.
        """
        logger.info('Retrieving airdrop', extra={'airdrop_id': airdrop_id})

        # Find document matching filter
        airdrop = self.collection.find_one(filter={'_id': airdrop_id})
        if not airdrop:
            raise NotFoundError

        # Convert to JSON
        airdrop = self.Model(**airdrop).to_json()

        return airdrop

    def update(self, airdrop_id: str, body: dict) -> dict:
        """Update a airdrop. If the airdrop does not exist, create a new airdrop.

        Args:
            airdrop_id (str): The id of the airdrop to update.
            body (dict): The fields to body.

        Returns:
            dict: The airdrop.

        Raises:
            NotFoundError: If the airdrop does not exist.
        """
        logger.info('Updating airdrop', extra={'airdrop_id': airdrop_id})

        # Find document matching filter
        airdrop = self.collection.find_one(filter={'_id': airdrop_id})
        if not airdrop:
            raise NotFoundError

        # Update fields
        airdrop = {**airdrop, **body}
        airdrop['updated'] = int(time.time())

        # Validate against schema
        validated_airdrop = self.Model(**airdrop)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': airdrop_id},
            update={'$set': validated_airdrop.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def complete(self, airdrop_id: str) -> dict:
        """Complete an airdrop.

        Args:
            airdrop_id (str): The id of the airdrop to complete.

        Returns:
            dict: The airdrop.
        """

        # Update status to 'complete'
        data = self.collection.find_one_and_update(
            filter={'_id': airdrop_id},
            update={'$set': {'status': 'complete'}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def send(self, airdrop_id: str) -> dict:
        """Send an airdrop.

        Args:
            airdrop_id (str): The id of the airdrop to send.

        Returns:
            dict: The airdrop.
        """

        # Get airdrop
        airdrop = self.retrieve_by_id(airdrop_id)
        account_id = airdrop['account']
        airdrop_id = airdrop['id']
        product_id = airdrop['product']
        conditions = airdrop['recipients']['segment_options']['conditions']
        email_settings = airdrop['email_settings']

        # Get product being airdropped
        product = self.product_service.retrieve_by_id(product_id)

        # Get list of recipients
        contacts = self.get_recipients(account_id, conditions)
        mint_list = []
        mints_available = 0
        for contact in contacts:
            # TODO: Update to allow more than one mint per email
            mints_available += 1
            mint_list.append({
                'email': contact['email'],
                'mints_available': 1,
                'mints_reserved': 0,
            })

        # Create mint link for airdrop
        mint_link_body = {
            'account': account_id,
            'airdrop': airdrop_id,
            'mint_list': mint_list,
            'mints_available': mints_available,
            'mints_reserved': 0,
            'name': product['name'] + ' Airdrop',
            'product': product_id,
            'public_mint': False,
        }
        mint_link = self.mint_link_service.create(mint_link_body)

        # Send emails to recipients
        for contact in contacts:
            self.send_email(contact, email_settings, product, mint_link)

        # Update status to 'complete'
        data = self.collection.find_one_and_update(
            filter={'_id': airdrop_id},
            update={'$set': {
                'mint_link': mint_link['id'],
                'status': 'complete'
            }},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def get_recipients(self, account_id: str, conditions: list) -> list:
        """Get a list of contacts from a segment.

        Args:
            account_id (str): The id of the account.
            conditions (dict): The conditions of the segment.

        Returns:
            list: The list of contacts.
        """
        logger.info('Getting segment', extra={'conditions': conditions})
        vql = conditions

        response = self.contact_service.list_segment_contacts(account_id, vql)
        logger.info(response)

        return response or []

    def send_email(self, contact, email_settings, product, mint_link):
        """Send an airdrop notice email to a recipient.

        Args:
            contact (_type_): _description_
            email_settings (_type_): _description_
            product (_type_): _description_
            mint_link (_type_): _description_

        Returns:
            _type_: _description_
        """
        logger.info('Sending email', extra={'email_settings': email_settings})

        content = email_settings.get('content')
        from_email = email_settings.get('from_email')
        from_image = email_settings.get('from_image')
        from_name = email_settings.get('from_name')
        preview_text = email_settings.get('preview_text')
        subject_line = email_settings.get('subject_line')
        to_name = contact.get('first_name')
        greeting = 'Hi there'
        if to_name:
            greeting = 'Hi ' + to_name.capitalize()

        body = {
            'template_name': 'airdrop',
            'template_content': [],
            'message': {
                'from_email': from_email,
                'from_name': from_name,
                'subject': subject_line,
                'to': [
                    {
                        'email': contact['email'],
                        'type': 'to'
                    }
                ],
                'merge_language': 'handlebars',
                'global_merge_vars': [
                    {
                        'name': 'CLAIM_URL',
                        'content': mint_link['url']
                    },
                    {
                        'name': 'FROM_NAME',
                        'content': from_name
                    },
                    {
                        'name': 'FROM_IMAGE',
                        'content': from_image
                    },
                    {
                        'name': 'GREETING',
                        'content': greeting
                    },
                    {
                        'name': 'MESSAGE',
                        'content': content
                    },
                    {
                        'name': 'PREVIEW_TEXT',
                        'content': preview_text
                    },
                    {
                        'name': 'PRODUCT_DESCRIPTION',
                        'content': product['description']
                    },
                    {
                        'name': 'PRODUCT_IMAGE',
                        'content': product['image']
                    },
                    {
                        'name': 'PRODUCT_NAME',
                        'content': product['name']
                    }
                ]
            }
        }
        logger.info(body)

        message = mailchimp.messages.send_template(body)
        logger.info(message)

        return message

    def delete(self, airdrop_id: str) -> bool:
        """Delete an airdrop.

        Args:
            airdrop_id (str): The id of the airdrop to delete.

        Returns:
            bool: True if the airdrop was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': airdrop_id
        })
        if not deleted:
            raise NotFoundError

        return True
