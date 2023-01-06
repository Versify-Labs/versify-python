import logging
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import RewardConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class RewardService(ExpandableResource):
    def __init__(self) -> None:
        self.collection = mdb[RewardConfig.db][RewardConfig.collection]
        self.expandables = RewardConfig.expandables
        self.Model = RewardConfig.model
        self.object = RewardConfig.object
        self.prefix = RewardConfig.prefix
        self.search_index = RewardConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new reward. If the reward already exists, update the reward.

        Args:
            reward (dict): The reward to create.

        Returns:
            dict: The reward.
        """
        logging.info("Creating reward", extra={"body": body})

        # Create fields
        reward_id = f"{self.prefix}_{ObjectId()}"
        body["_id"] = reward_id
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
        """Count rewards.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of rewards.
        """
        logging.info("Counting rewards", extra={"filter": filter})

        # Get rewards from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List rewards.

        Args:
            query (dict): The query to use.

        Returns:
            list: The rewards.
        """
        logging.info("Listing rewards", extra={"filter": filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort("_id", -1).limit(limit).skip(skip)

        # Convert cursor to list
        rewards = [self.Model(**doc).to_json() for doc in cursor]

        return rewards

    def get(self, reward_id: str) -> dict:
        """Get an reward by id.

        Args:
            reward_id (str): The id of the reward to retrieve.

        Returns:
            dict: The reward.
        """
        logging.info("Retrieving reward", extra={"reward_id": reward_id})

        # Find document matching filter
        reward = self.collection.find_one(filter={"_id": reward_id})
        if not reward:
            raise NotFoundError

        # Convert to JSON
        reward = self.Model(**reward).to_json()

        return reward

    def update(self, reward_id: str, body: dict) -> dict:
        """Update a reward. If the reward does not exist, create a new reward.

        Args:
            reward_id (str): The id of the reward to update.
            body (dict): The fields to update.

        Returns:
            dict: The reward.

        Raises:
            NotFoundError: If the reward does not exist.
        """
        logging.info("Updating reward", extra={"reward_id": reward_id})

        # Find document matching filter
        reward = self.collection.find_one(filter={"_id": reward_id})
        if not reward:
            raise NotFoundError

        # Update fields
        reward = deep_update(reward, body)
        reward["updated"] = int(time.time())

        # Validate against schema
        validated_reward = self.Model(**reward)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={"_id": reward_id},
            update={"$set": validated_reward.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, reward_id: str) -> bool:
        """Delete an reward.

        Args:
            reward_id (str): The id of the reward to delete.

        Returns:
            bool: True if the reward was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({"_id": reward_id})
        if not deleted:
            raise NotFoundError

        return True
