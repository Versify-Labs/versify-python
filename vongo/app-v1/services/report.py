import logging
import time

from bson.objectid import ObjectId

from ..config import ReportConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb


class ReportService(ExpandableResource):
    def __init__(self) -> None:
        self.collection = mdb[ReportConfig.db][ReportConfig.collection]
        self.expandables = ReportConfig.expandables
        self.Model = ReportConfig.model
        self.object = ReportConfig.object
        self.prefix = ReportConfig.prefix
        self.search_index = ReportConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new report. If the report already exists, update the report.

        Args:
            body (dict): The report to create.

        Returns:
            dict: The report.
        """
        logging.info("Creating report", extra={"report": body})

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
        """Count reports.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of reports.
        """
        logging.info("Counting reports", extra={"filter": filter})

        # Get reports from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List reports.

        Args:
            query (dict): The query to use.

        Returns:
            list: The reports.
        """
        logging.info("Listing reports", extra={"filter": filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort("_id", -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def retrieve_by_id(self, report_id: str) -> dict:
        """Get an report by id.

        Args:
            report_id (str): The id of the report to retrieve.

        Returns:
            dict: The report.
        """
        logging.info("Retrieving report", extra={"id": report_id})

        # Find document matching filter
        report = self.collection.find_one(filter={"_id": report_id})
        if not report:
            raise NotFoundError

        # Convert to JSON
        report = self.Model(**report).to_json()

        return report

    def delete(self, report_id: str) -> bool:
        """Delete an report.

        Args:
            report_id (str): The id of the report to delete.

        Returns:
            bool: True if the report was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({"_id": report_id})
        if not deleted:
            raise NotFoundError

        return True
