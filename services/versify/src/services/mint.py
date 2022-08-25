import datetime
import time

import simplejson as json
from aws_lambda_powertools import Logger, Tracer
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import NotFoundError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb
from ..utils.tatum import Tatum

logger = Logger()
tracer = Tracer()


class MintService(ExpandableResource):

    def __init__(
        self,
        airdrop_service,
        contact_service,
        mint_link_service,
    ) -> None:
        _config = config['mint']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

        # Internal services
        self.airdrop_service = airdrop_service
        self.contact_service = contact_service
        self.mint_link_service = mint_link_service

    def create(self, body: dict) -> dict:
        """Create a new mint. If the mint already exists, update the mint.

        Args:
            body (dict): The mint to create.

        Returns:
            dict: The mint.
        """
        logger.info('Creating mint', extra={'body': body})

        # Create universal fields
        mint_id = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['_id'] = mint_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        account_id = None
        email = body['email']
        wallet_address = body['wallet_address']
        if body.get('mint_link'):
            mint_link_id = body['mint_link']
            mint_link = self.mint_link_service.retrieve_by_id(mint_link_id)
            account_id = mint_link['account']

            # Not all mint links are from airdrops
            body['airdrop'] = mint_link.get('airdrop')

            # Reserve mints for specific user email
            self.mint_link_service.reserve_mints(mint_link_id, email, 1)

        body['account'] = account_id

        # Upsert contact and add it to mint
        contact_body = {'account': account_id, 'email': email}
        if wallet_address:
            contact_body['wallet_address'] = wallet_address
        contact = self.contact_service.create(contact_body)
        body['contact'] = contact['id']

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Fulfill mint and return
        return self.fulfill(mint_id)

    def count(self, filter: dict) -> int:
        """Count mints.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of mints.
        """
        logger.info('Counting mints', extra={'filter': filter})

        # Get mints from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List mints.

        Args:
            filter (dict): The filter to use.

        Returns:
            list: The mints.
        """
        logger.info('Listing mints', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def update(self, mint_id: str, body: dict) -> dict:
        """Update a mint. If the mint does not exist, create a new mint.

        Args:
            mint_id (str): The id of the mint to update.
            body (dict): The fields to update.

        Returns:
            dict: The mint.

        Raises:
            NotFoundError: If the mint does not exist.
        """
        logger.info('Updating mint', extra={'mint_id': mint_id})

        # Find document matching filter
        mint = self.collection.find_one(filter={'_id': mint_id})
        if not mint:
            raise NotFoundError

        # Update fields
        mint = {**mint, **body}
        mint['updated'] = int(time.time())

        # Validate against schema
        validated_mint = self.Model(**mint)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': mint_id},
            update={'$set': validated_mint.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def fulfill(self,  mint_id: str) -> dict:

        # Get the mint, product, and collection
        mint = self.retrieve_by_id(mint_id)
        mint = self.expand(mint, ['product.collection'])
        product = mint['product']
        collection = product['collection']
        wallet_address = mint['wallet_address']

        # Mint token to contract
        tatum = Tatum()
        response = tatum.mint_token(
            contract=collection['contract_address'],
            token=product['token_id'],
            to=wallet_address
        )
        signature = response.get('signatureId')

        # Update collection with txn result
        data = self.collection.find_one_and_update(
            filter={'_id': mint_id},
            update={'$set': {
                'signature': signature,
                'status': 'pending' if signature else 'failed'
            }},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def retrieve_by_id(self, mint_id: str) -> dict:
        """Get an mint by id.

        Args:
            mint_id (str): The id of the mint to retrieve.

        Returns:
            dict: The mint.
        """
        logger.info('Retrieving mint', extra={'mint_id': mint_id})

        # Find document matching filter
        mint = self.collection.find_one(filter={'_id': mint_id})
        if not mint:
            raise NotFoundError

        # Convert to JSON
        mint = self.Model(**mint).to_json()

        return mint

    def generate_report(self, account_id, vql):
        """Generate a report of mints."""

        days = 7
        for clause in vql.split(' '):
            if 'days:' in clause:
                days = int(clause[5:])

        report = {}
        now = datetime.datetime.now()
        date_str = ""
        for x in range(days):
            d = now - datetime.timedelta(days=x)
            date_str = d.strftime("%Y-%m-%d")
            report[date_str] = 0
        date_format = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        unix_time = datetime.datetime.timestamp(date_format)

        stages = [
            {
                "$match": {
                    'account': account_id,
                    'created': {"$gt": unix_time}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {
                                "$toDate": {
                                    "$multiply": [1000, "$created"]
                                }
                            }
                        }
                    },
                    "count": {"$sum": 1}
                }
            }
        ]
        cursor = self.collection.aggregate(stages)
        result = json.loads(dumps(list(cursor)))
        for r in result:
            report[r['_id']] = r['count']
        return report

    def delete(self, mint_id: str) -> bool:
        """Delete an mint.

        Args:
            mint_id (str): The id of the mint to delete.

        Returns:
            bool: True if the mint was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': mint_id
        })
        if not deleted:
            raise NotFoundError

        return True
