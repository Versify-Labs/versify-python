import logging
import time

from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..config import MintLinkConfig
from ..utils.exceptions import NotFoundError, UsageLimitError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class MintLinkService(ExpandableResource):
    def __init__(self, account_service) -> None:
        self.collection = mdb[MintLinkConfig.db][MintLinkConfig.collection]
        self.expandables = MintLinkConfig.expandables
        self.Model = MintLinkConfig.model
        self.object = MintLinkConfig.object
        self.prefix = MintLinkConfig.prefix
        self.search_index = MintLinkConfig.search_index

        # Internal Services
        self.account_service = account_service

    def create(self, body: dict) -> dict:
        """Create a new mint_link. If the mint_link already exists, update the mint_link.

        Args:
            mint_link (dict): The mint_link to create.

        Returns:
            dict: The mint_link.
        """
        logging.info("Creating mint_link", extra={"body": body})

        # Create fields
        mint_link_id = f"{self.prefix}_{ObjectId()}"
        body["_id"] = mint_link_id
        body["created"] = int(time.time())
        body["updated"] = int(time.time())

        # Get account
        account_id = body["account"]
        account = self.account_service.retrieve_by_id(account_id)
        account_name = account["name"]
        account_icon = account["branding"].get("icon")
        account_logo = account["branding"].get("logo")

        # Inject with necessary fields
        branding = body.get("branding", {})
        branding["background_color"] = branding.get("background_color", "#E1E4FF")
        branding["button_color"] = branding.get("button_color", "#596AFF")
        branding["font"] = branding.get("font", "inherit")
        branding["icon"] = branding.get("icon", account_icon)
        branding["logo"] = branding.get("logo", account_logo)
        branding["name"] = branding.get("name", account_name)
        branding["shapes"] = branding.get("shapes", "rounded")
        body["branding"] = branding
        body["url"] = MintLinkConfig.MINT_URL + "/" + body["_id"]

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
        logging.info("Counting mint_links", extra={"filter": filter})

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
        logging.info("Listing mint_links", extra={"filter": filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort("_id", -1).limit(limit).skip(skip)

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
        logging.info("Updating mint_link")

        # Find document matching filter
        mint_link = self.collection.find_one(filter={"_id": mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Update fields
        mint_link = {**mint_link, **body}
        mint_link["updated"] = int(time.time())

        # Validate against schema
        data = self.Model(**mint_link)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={"_id": mint_link_id},
            update={"$set": data.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
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

        Raises:
            NotFoundError: If the mint_link does not exist.
        """
        logging.info("Archiving mint_link")

        # Find document matching filter
        mint_link = self.collection.find_one(filter={"_id": mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Update item in DB
        mint_link = self.collection.find_one_and_update(
            filter={"_id": mint_link_id},
            update={
                "$set": {"active": False, "archived": True, "updated": int(time.time())}
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
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
        logging.info("Reserving mints")

        # Find document matching filter
        mint_link = self.collection.find_one(filter={"_id": mint_link_id})
        if not mint_link:
            raise NotFoundError

        # Get fields to be updated
        active = mint_link.get("active", False)
        mint_list = mint_link.get("mint_list", [])
        mints_available = mint_link.get("mints_available", 0)
        mints_reserved = mint_link.get("mints_reserved", 0)

        # Verify/update aggregate fields
        if mints_available < mint_count:
            raise UsageLimitError
        mints_available -= mint_count
        mints_reserved += mint_count
        if mints_available <= 0:
            active = False

        # Verify/update email specific fields
        for i, spot in enumerate(mint_list):
            if spot["email"] == email:
                if spot["mints_available"] < mint_count:
                    raise UsageLimitError
                spot["mints_available"] -= mint_count
                spot["mints_reserved"] += mint_count
                mint_list[i] = spot
                break

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={"_id": mint_link_id},
            update={
                "$set": {
                    "active": active,
                    "mint_list": mint_list,
                    "mints_available": mints_available,
                    "mints_reserved": mints_reserved,
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
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
        logging.info("Retrieving mint_link")

        # Find document matching filter
        mint_link = self.collection.find_one(filter={"_id": mint_link_id})
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
        deleted = self.collection.find_one_and_delete({"_id": mint_link_id})
        if not deleted:
            raise NotFoundError

        return True
