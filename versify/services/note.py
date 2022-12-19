import logging
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import NoteConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class NoteService(ExpandableResource):

    def __init__(self) -> None:
        self.collection = mdb[NoteConfig.db][NoteConfig.collection]
        self.expandables = NoteConfig.expandables
        self.Model = NoteConfig.model
        self.object = NoteConfig.object
        self.prefix = NoteConfig.prefix
        self.search_index = NoteConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new note. If the note already exists, update the note.

        Args:
            note (dict): The note to create.

        Returns:
            dict: The note.
        """
        logging.info('Creating note', extra={'body': body})

        # Create fields
        note_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = note_id
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
        """Count notes.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of notes.
        """
        logging.info('Counting notes', extra={'filter': filter})

        # Get notes from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List notes.

        Args:
            query (dict): The query to use.

        Returns:
            list: The notes.
        """
        logging.info('Listing notes', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        notes = [self.Model(**doc).to_json() for doc in cursor]

        return notes

    def retrieve_by_id(self, note_id: str) -> dict:
        """Get an note by id.

        Args:
            note_id (str): The id of the note to retrieve.

        Returns:
            dict: The note.
        """
        logging.info('Retrieving note', extra={'note_id': note_id})

        # Find document matching filter
        note = self.collection.find_one(filter={'_id': note_id})
        if not note:
            raise NotFoundError

        # Convert to JSON
        note = self.Model(**note).to_json()

        return note

    def update(self, note_id: str, body: dict) -> dict:
        """Update a note. If the note does not exist, create a new note.

        Args:
            note_id (str): The id of the note to update.
            body (dict): The fields to update.

        Returns:
            dict: The note.

        Raises:
            NotFoundError: If the note does not exist.
        """
        logging.info('Updating note', extra={'note_id': note_id})

        # Find document matching filter
        note = self.collection.find_one(filter={'_id': note_id})
        if not note:
            raise NotFoundError

        # Update fields
        note = deep_update(note, body)
        note['updated'] = int(time.time())

        # Validate against schema
        validated_note = self.Model(**note)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': note_id},
            update={'$set': validated_note.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, note_id: str) -> bool:
        """Delete an note.

        Args:
            note_id (str): The id of the note to delete.

        Returns:
            bool: True if the note was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': note_id
        })
        if not deleted:
            raise NotFoundError

        return True
