import datetime
import logging
import time

import simplejson as json
from bson.json_util import dumps
from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import MintConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb
from ..utils.tatum import Tatum


class MintService(ExpandableResource):
    def __init__(
        self,
        airdrop_service,
        contact_service,
        mint_link_service,
        product_service,
        user_service,
    ) -> None:
        self.collection = mdb[MintConfig.db][MintConfig.collection]
        self.expandables = MintConfig.expandables
        self.Model = MintConfig.model
        self.object = MintConfig.object
        self.prefix = MintConfig.prefix
        self.search_index = MintConfig.search_index

        # Internal services
        self.airdrop_service = airdrop_service
        self.contact_service = contact_service
        self.mint_link_service = mint_link_service
        self.product_service = product_service
        self.user_service = user_service

    def create(self, body: dict) -> dict:
        """Create a new mint.

        Args:
            body (dict): The mint to create.

        Returns:
            dict: The mint.
        """
        logging.info("Creating mint")

        # Create universal fields
        mint_id = body.get("_id", f"{self.prefix}_{ObjectId()}")
        account_id = body.get("account", None)
        body["_id"] = mint_id
        body["account"] = account_id
        body["created"] = int(time.time())
        body["updated"] = int(time.time())

        contact_id = body.get("contact")
        email = body.get("email")
        if not contact_id and not email:
            raise ValueError("Must provide either contact or email")

        # Get users managed wallet address if not provided
        if not email:
            contact = self.contact_service.get(contact_id)
            email = contact["email"]
        user = self.user_service.get(email)
        wallet_address = None
        for wallet in user["wallets"]:
            if "managed" in wallet and wallet["managed"]:
                wallet_address = wallet["address"]
                body["wallet_address"] = wallet_address
                break

        # TODO: Remove this as mint links will be deprecated
        if body.get("mint_link"):
            mint_link_id = body["mint_link"]
            mint_link = self.mint_link_service.retrieve_by_id(mint_link_id)

            # Not all mint links are from airdrops
            body["airdrop"] = mint_link.get("airdrop")

            # Reserve mints for specific user email
            self.mint_link_service.reserve_mints(mint_link_id, email, 1)

        # Upsert contact and add it to mint
        contact_body = {
            "account": account_id,
            "email": email,
            "wallet_address": wallet_address,
        }
        contact = self.contact_service.create(contact_body)
        body["contact"] = contact["id"]

        # Get the product and collection
        product = self.product_service.retrieve_by_id(body["product"])
        product = self.product_service.expand(product, ["collection"])
        collection = product["collection"]

        # Mint token to contract
        tatum = Tatum()
        response = tatum.mint_token(
            contract=collection["contract_address"],
            token=product["token_id"],
            to=wallet_address,
        )
        signature = response.get("signatureId")

        # Update mint with txn result
        body["signature"] = signature
        body["status"] = "pending" if signature else "failed"

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count mints.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of mints.
        """
        logging.info("Counting mints")

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
        logging.info("Listing mints")

        # Find documents matching filter
        cursor = self.collection.find(filter).sort("_id", -1).limit(limit).skip(skip)

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
        logging.info("Updating mint")

        # Find document matching filter
        mint = self.collection.find_one(filter={"_id": mint_id})
        if not mint:
            raise NotFoundError

        # Update fields
        mint = deep_update(mint, body)
        mint["updated"] = int(time.time())

        # Validate against schema
        validated_mint = self.Model(**mint)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={"_id": mint_id},
            update={"$set": validated_mint.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
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
        logging.info("Retrieving mint")

        # Find document matching filter
        mint = self.collection.find_one(filter={"_id": mint_id})
        if not mint:
            raise NotFoundError

        # Convert to JSON
        mint = self.Model(**mint).to_json()

        return mint

    def generate_report(self, account_id, vql):
        """Generate a report of mints."""

        days = 7
        for clause in vql.split(" "):
            if "days:" in clause:
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
            {"$match": {"account": account_id, "created": {"$gt": unix_time}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {"$toDate": {"$multiply": [1000, "$created"]}},
                        }
                    },
                    "count": {"$sum": 1},
                }
            },
        ]
        cursor = self.collection.aggregate(stages)
        result = json.loads(dumps(list(cursor)))
        for r in result:
            report[r["_id"]] = r["count"]
        return report

    def delete(self, mint_id: str) -> bool:
        """Delete an mint.

        Args:
            mint_id (str): The id of the mint to delete.

        Returns:
            bool: True if the mint was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({"_id": mint_id})
        if not deleted:
            raise NotFoundError

        return True
