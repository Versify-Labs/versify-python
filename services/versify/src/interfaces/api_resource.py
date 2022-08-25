import time
from typing import Any, Optional

from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import (ExpansionDepthError, ExpansionResourceError,
                          NotFoundError)
from ..services._config import config
from ..utils.mongo import mdb


class ApiResource:

    def __init__(
        self,
        db_name: str,
        db_collection: str,
        expandables: list,
        object: str,
        prefix: str,
        model: Any,
        search_index: Optional[str]
    ):
        self.collection = mdb[db_name][db_collection]
        self.expandables = expandables
        self.object = object
        self.prefix = prefix
        self.Model = model
        self.search_index = search_index

    def count(self, filter: dict) -> int:
        return self.collection.count_documents(filter)

    def pre_create(self, body: dict, auth: dict = {}) -> dict:
        return body

    def post_create(self, body: dict, auth: dict = {}) -> dict:
        return body

    def pre_update(self, body: dict, filter: dict = {}) -> dict:
        return body

    def post_update(self, body: dict, filter: dict = {}) -> dict:
        return body

    def get_resource_obj(self, obj_type, obj_id, organization=None):
        resource_cfg = config[obj_type]
        resource_collection = mdb[resource_cfg.db][resource_cfg.collection]
        resource_model = resource_cfg.model

        # Create query params
        query = {'_id': obj_id}
        if organization:
            query['organization'] = organization

        # Find resource in collection
        found = resource_collection.find_one(query)
        if not found:
            return None

        return resource_model(**found).to_json()

    def expand_object(self, data, path=''):
        resources_left = path.split('.')

        # Base Case
        if len(resources_left) < 1 or resources_left == ['']:
            return data

        # Depth Limit
        if len(resources_left) > 4:
            raise ExpansionDepthError

        # Validate the resource requested can be expanded
        parent_object = data['object']
        child_object = resources_left[0]
        cfg = config[parent_object]
        if child_object not in cfg.expandables:
            raise ExpansionResourceError(parent_object, child_object)

        resource_id = data[child_object]
        if type(resource_id) != str:
            return data

        next_path = '.'.join(resources_left[1:])
        resource_obj = self.get_resource_obj(child_object, resource_id)
        data[child_object] = self.expand_object(resource_obj, next_path)
        return data

    def expand(self, data, expand_list):
        if type(data) == list:
            data = {'data': data, 'object': 'list'}
        for path in expand_list:
            if path.startswith('data'):
                new_data = []
                new_path = path[5:]
                for obj in data['data']:  # type: ignore

                    new_data.append(self.expand_object(obj, new_path))
                data['data'] = new_data  # type: ignore
            else:
                data = self.expand_object(data, path)
        return data

    def find(self, filter: dict, limit: int = 20, skip: int = 0) -> list:
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)
        return [self.Model(**doc).to_json() for doc in cursor]

    def create(self, body: dict, expand_list: list = [], auth: dict = {}) -> dict:

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['account'] = body.get('account') or auth.get('account')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Enrich payload data with object specific fields
        body = self.pre_create(body, auth)

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        # Post processing of newly created object
        self.post_create(data, auth)

        # Expand and return data
        return self.expand(data, expand_list)  # type: ignore

    def delete(self, filter: dict) -> bool:

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete(filter)
        if not deleted:
            raise NotFoundError

        return True

    def get(self, filter: dict, expand_list: list = []) -> dict:

        # Find document matching filter
        data = self.collection.find_one(filter)
        if not data:
            raise NotFoundError

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        return self.expand(data, expand_list)  # type: ignore

    def list(
        self,
        filter: dict = {},
        limit: int = 20,
        skip: int = 0,
        expand_list: list = []
    ) -> list:

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        # Convert to JSON and expand fields
        data = self.expand(data, expand_list)  # type: ignore
        return data.get('data', [])  # type: ignore

    def update(
        self,
        body: dict,
        filter: dict,
        expand_list=[]
    ) -> dict:

        # Get document matching filter
        data = self.get(filter)

        # Pre processing of object being updated
        body = self.pre_update(body, filter)

        # Update data with payload
        body['updated'] = int(time.time())
        data.update(body)

        # Update document in DB
        data = self.collection.find_one_and_update(
            filter,
            {'$set': self.Model(**data).to_bson()},
            return_document=ReturnDocument.AFTER,
        )

        # Post processing of updated object
        self.post_update(data, filter)

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        
        return self.expand(data, expand_list)  # type: ignore
