from pprint import pprint
from typing import Any, Dict, List, Optional, Tuple, Union

from ..db.session import SessionLocal
from ..models.enums import Operator
from ..models.factory import current_timestamp
from pymongo import ASCENDING, ReturnDocument


class BaseResource:
    def __init__(self, db_session: SessionLocal):
        db_name = self.__class__.__module__.split(".")[1]
        db_collection = self.__class__.__name__.lower()
        self.collection = db_session.get_collection(db_name, db_collection)

    def _parse_filters(self, **filters: Dict[str, Any]) -> Dict[str, Any]:
        filters_copy = filters.copy()
        for key, value in filters_copy.items():
            if value is None:
                del filters[key]
            elif isinstance(value, list):
                filters[key] = {"$in": value}
            elif isinstance(value, str):
                filters[key] = {"$regex": value}
        return filters

    def _parse_query(self, query: Dict[str, Any] = {}) -> dict:
        # TODO: Handle custom fields

        print()
        print("Query:")
        pprint(query)

        field = query.get("field")
        operator = query.get("operator")
        value = query.get("value")
        print("field:", field)
        print("operator:", operator)
        print("value:", value)

        # Handle logical operators
        if operator == Operator.AND and isinstance(value, list):
            return {"$and": [self._parse_query(q) for q in value]}
        elif operator == Operator.OR and isinstance(value, list):
            return {"$or": [self._parse_query(q) for q in value]}
        elif operator == Operator.NOT and isinstance(value, dict):
            return {"$not": self._parse_query(value)}

        # Handle all types
        elif operator == Operator.EQUALS:
            return {field: value}
        elif operator == Operator.NOT_EQUALS:
            return {field: {"$ne": value}}
        elif operator == Operator.EXISTS:
            return {field: {"$exists": True}}
        elif operator == Operator.NOT_EXISTS:
            return {field: {"$exists": False}}

        # Handle strings
        elif operator == Operator.CONTAINS:
            return {field: {"$regex": value}}
        elif operator == Operator.NOT_CONTAINS:
            return {field: {"$not": {"$regex": value}}}
        elif operator == Operator.STARTS_WITH:
            return {field: {"$regex": f"^{value}"}}
        elif operator == Operator.NOT_STARTS_WITH:
            return {field: {"$not": {"$regex": f"^{value}"}}}
        elif operator == Operator.ENDS_WITH:
            return {field: {"$regex": f"{value}$"}}
        elif operator == Operator.NOT_ENDS_WITH:
            return {field: {"$not": {"$regex": f"{value}$"}}}

        # Handle numbers
        elif operator == Operator.GREATER_THAN:
            return {field: {"$gt": value}}
        elif operator == Operator.GREATER_THAN_OR_EQUAL:
            return {field: {"$gte": value}}
        elif operator == Operator.LESS_THAN:
            return {field: {"$lt": value}}
        elif operator == Operator.LESS_THAN_OR_EQUAL:
            return {field: {"$lte": value}}

        # Handle lists
        elif operator == Operator.IN:
            return {field: {"$in": value}}
        elif operator == Operator.NOT_IN:
            return {field: {"$nin": value}}

        # Return empty dict if no match
        else:
            return {}

    def _create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["created"] = current_timestamp()
        data["updated"] = current_timestamp()
        return self.collection.insert_one(data).inserted_id

    def _count(
        self,
        **filters: Dict[str, Any],
    ) -> int:
        filters = self._parse_filters(**filters)
        return self.collection.count_documents(filters)

    def _delete(
        self,
        **filters: Dict[str, Any],
    ) -> bool:
        filters = self._parse_filters(**filters)
        deleted = self.collection.delete_one(filters).deleted_count
        return deleted > 0

    def _get(
        self,
        **filters: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        filters = self._parse_filters(**filters)
        return self.collection.find_one(filters)

    def _list(
        self,
        page_num: Union[int, None] = None,
        page_size: Union[int, None] = None,
        sort: List[Tuple[str, int]] = [("created", ASCENDING)],
        **filters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        list_args = {}
        if page_num is not None and page_size is not None:
            list_args["limit"] = page_size
            list_args["skip"] = (page_num - 1) * page_size
        if sort:
            list_args["sort"] = sort
        filters = self._parse_filters(**filters)
        return list(self.collection.find(filters, **list_args))

    def _search(
        self,
        page_num: Union[int, None] = None,
        page_size: Union[int, None] = None,
        account: Union[str, None] = None,
        query: Dict[str, Any] = {},
    ) -> List[Dict[str, Any]]:
        list_args = {}
        if page_num is not None and page_size is not None:
            list_args["limit"] = page_size
            list_args["skip"] = (page_num - 1) * page_size
        filters = self._parse_query(query)
        if account:
            filters["account"] = account
        print()
        print("Filters:")
        pprint(filters)
        return list(self.collection.find(filters, **list_args))

    def _update(self, id: str, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates = {}
        for key, value in body.items():
            if value is not None:
                updates[key] = value
        if not updates or len(updates.keys()) < 1:
            return self.collection.find_one({"_id": id})
        updates["updated"] = current_timestamp()
        return self.collection.find_one_and_update(
            filter={"_id": id},
            update={"$set": updates},
            return_document=ReturnDocument.AFTER,
        )
