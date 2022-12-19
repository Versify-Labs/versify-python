import logging
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import ClaimConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class ClaimService(ExpandableResource):

    def __init__(self, contact_service) -> None:
        self.collection = mdb[ClaimConfig.db][ClaimConfig.collection]
        self.expandables = ClaimConfig.expandables
        self.Model = ClaimConfig.model
        self.object = ClaimConfig.object
        self.prefix = ClaimConfig.prefix
        self.search_index = ClaimConfig.search_index

        # Internal services
        self.contact_service = contact_service

    def create(self, body: dict) -> dict:
        """Create a new claim.

        Args:
            body (dict): The claim to create.

        Returns:
            dict: The claim.
        """
        logging.info('Creating claim', extra={'body': body})

        # TODO: Check if user already submitted a claim
        # TODO: Submit the claim event
        # TODO: Return the result

        # Create universal fields
        claim_id = body.get('_id', f'{self.prefix}_{ObjectId()}')
        email = body['email']
        body['_id'] = claim_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Upsert contact and add it to claim
        account_id = body['account']
        contact_body = {
            'account': account_id,
            'email': email,
        }
        contact = self.contact_service.create(contact_body)
        body['contact'] = contact['id']

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count claims.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of claims.
        """
        logging.info('Counting claims', extra={'filter': filter})

        # Get claims from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List claims.

        Args:
            filter (dict): The filter to use.

        Returns:
            list: The claims.
        """
        logging.info('Listing claims', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def update(self, claim_id: str, body: dict) -> dict:
        """Update a claim. If the claim does not exist, create a new claim.

        Args:
            claim_id (str): The id of the claim to update.
            body (dict): The fields to update.

        Returns:
            dict: The claim.

        Raises:
            NotFoundError: If the claim does not exist.
        """
        logging.info('Updating claim', extra={'claim_id': claim_id})

        # Find document matching filter
        claim = self.collection.find_one(filter={'_id': claim_id})
        if not claim:
            raise NotFoundError

        # Update fields
        claim = deep_update(claim, body)
        claim['updated'] = int(time.time())

        # Validate against schema
        validated_claim = self.Model(**claim)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': claim_id},
            update={'$set': validated_claim.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def retrieve_by_id(self, claim_id: str) -> dict:
        """Get an claim by id.

        Args:
            claim_id (str): The id of the claim to retrieve.

        Returns:
            dict: The claim.
        """
        logging.info('Retrieving claim', extra={'claim_id': claim_id})

        # Find document matching filter
        claim = self.collection.find_one(filter={'_id': claim_id})
        if not claim:
            raise NotFoundError

        # Convert to JSON
        claim = self.Model(**claim).to_json()

        return claim

    def delete(self, claim_id: str) -> bool:
        """Delete an claim.

        Args:
            claim_id (str): The id of the claim to delete.

        Returns:
            bool: True if the claim was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': claim_id
        })
        if not deleted:
            raise NotFoundError

        return True
