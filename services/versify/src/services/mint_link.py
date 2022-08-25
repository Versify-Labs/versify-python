import os
import time

from aws_lambda_powertools import Logger, Tracer
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import NotFoundError, UsageLimitError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb

logger = Logger()
tracer = Tracer()

if os.environ.get('ENVIRONMENT', 'dev') == 'prod':
    MINT_URL = 'https://mint.versifylabs.com'
else:
    MINT_URL = 'https://mint-dev.versifylabs.com'


class MintLinkService(ExpandableResource):

    def __init__(
        self,
        account_service
    ) -> None:
        _config = config['mint_link']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

        # Internal Services
        self.account_service = account_service

    def create(self, body: dict) -> dict:
        """Create a new mint_link. If the mint_link already exists, update the mint_link.

        Args:
            mint_link (dict): The mint_link to create.

        Returns:
            dict: The mint_link.
        """
        logger.info('Creating mint_link', extra={'body': body})

        # Create fields
        mint_link_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = mint_link_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Inject with necessary fields
        account_id = body['account']
        account = self.account_service.retrieve_by_id(account_id)
        business_branding = account['business_profile']['branding']
        body['branding'] = {
            'colors': {
                'background': business_branding['primary_color'],
                'button': business_branding['secondary_color']
            },
            'logo': business_branding.get('logo'),
            'name': account['business_profile']['name']
        }
        body['url'] = MINT_URL + '/' + body['_id']

        # Validate mints against account billing plan
        mint_count = body.get('mints_available', 1)
        self.account_service.reserve_mints(account_id, mint_count)

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count mint_links.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of mint_links.
        """
        logger.info('Counting mint_links', extra={'filter': filter})

        # Get mint_links from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List mint_links.

        Args:
            query (dict): The query to use.

        Returns:
            list: The mint_links.
        """
        logger.info('Listing mint_links', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        mint_links = [self.Model(**doc).to_json() for doc in cursor]

        return mint_links

    def update(self, mint_link_id: str, body: dict) -> dict:
        """Update a mint_link. If the mint_link does not exist, create a new mint_link.

        Args:
            mint_link_id (str): The id of the mint_link to update.
            body (dict): The fields to update.

        Returns:
            dict: The mint_link.

        Raises:
            NotFoundError: If the mint_link does not exist.
        """
        logger.info('Updating mint_link', extra={'mint_link_id': mint_link_id})

        # Find document matching filter
        mint_link = self.collection.find_one(filter={'_id': mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Update fields
        mint_link = {**mint_link, **body}
        mint_link['updated'] = int(time.time())

        # Validate against schema
        data = self.Model(**mint_link)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': mint_link_id},
            update={'$set': data.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def archive(self, mint_link_id: str) -> dict:
        """Archive a mint_link.

        Args:
            mint_link_id (str): The id of the mint_link to archive.

        Returns:
            dict: The mint_link.
        """
        logger.info('Archiving mint_link', extra={'id': mint_link_id})

        # Find document matching filter
        mint_link = self.collection.find_one(filter={'_id': mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Update item in DB
        mint_link = self.collection.find_one_and_update(
            filter={'_id': mint_link_id},
            update={'$set': {
                'active': False,
            }},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        mint_link = self.Model(**mint_link).to_json()

        return mint_link

    def reserve_mints(self, mint_link_id: str, email: str, mint_count: int) -> dict:
        """Verify and update the mint_link's mint stats.

        Args:
            mint_link_id (str): The id of the mint_link to update.
            mint_count (int): The number of mints to add to the mint_stats.
        """
        logger.info('Reserving mints', extra={'id': mint_link_id})

        # Find document matching filter
        mint_link = self.collection.find_one(filter={'_id': mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Get fields to be updated
        active = mint_link.get('active', False)
        mint_list = mint_link.get('mint_list', [])
        mints_available = mint_link.get('mints_available', 0)
        mints_reserved = mint_link.get('mints_reserved', 0)

        # Verify/update aggregate fields
        if mints_available < mint_count:
            raise UsageLimitError
        mints_available -= mint_count
        mints_reserved += mint_count
        if mints_available <= 0:
            mint_link['active'] = False

        # Verify/update email specific fields
        for i, spot in enumerate(mint_list):
            if spot['email'] == email:
                if spot['mints_available'] < mint_count:
                    raise UsageLimitError
                spot['mints_available'] -= mint_count
                spot['mints_reserved'] += mint_count
                mint_list[i] = spot
                break

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': mint_link_id},
            update={'$set': {
                'active': active,
                'mint_list': mint_list,
                'mints_available': mints_available,
                'mints_reserved': mints_reserved
            }},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def retrieve_by_id(self, mint_link_id: str) -> dict:
        """Get a mint_link by id.

        Args:
            mint_link_id (str): The id of the mint_link to retrieve.

        Returns:
            dict: The mint_link.
        """
        logger.info('Retrieving mint_link', extra={'id': mint_link_id})

        # Find document matching filter
        mint_link = self.collection.find_one(filter={'_id': mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Convert to JSON
        mint_link = self.Model(**mint_link).to_json()

        return mint_link

    def delete(self, mint_link_id: str) -> bool:
        """Delete an mint_link.

        Args:
            mint_link_id (str): The id of the mint_link to delete.

        Returns:
            bool: True if the mint_link was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': mint_link_id
        })
        if not deleted:
            raise NotFoundError

        return True
