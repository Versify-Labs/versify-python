import time

import simplejson as json
from aws_lambda_powertools import Logger
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..utils.expand import expand_object
from ..utils.mongo import mdb
from ..utils.pipelines import Pipeline
from .config import config
from .errors import NotFoundError

logger = Logger()


class ApiResource:

    def __init__(self, resource):
        cfg = config[resource]
        self.collection = mdb[cfg.db][cfg.collection]
        self.expandables = cfg.expandables
        self.object = cfg.object
        self.prefix = cfg.prefix or cfg.object
        self.Model = cfg.model
        self.search_index = cfg.search_index

    def expand_data(self, app, data):
        params = app.current_event.query_string_parameters or {}
        expand_list = params.get('expand', '').split(',')
        for path in expand_list:
            if path.startswith('data'):
                new_data = []
                new_path = path[5:]
                for obj in data['data']:
                    new_data.append(expand_object(obj, new_path))
                data['data'] = new_data
            else:
                data = expand_object(data, path)
        return data

    def inject_data(self, raw):
        return raw

    def list(self, app):
        params = app.current_event.query_string_parameters or {}
        organization = app.current_event.get_header_value('X-Organization')
        if organization:
            params['organization'] = organization

        # Pagination
        page_size = int(params.pop('page_size', 20))
        page_num = int(params.pop('page_num', 1))
        limit = page_size
        skip = page_size * (page_num - 1)

        # Query Filter
        query = params.pop('query', '')
        filters = query.split(',')
        filters = [f for f in filters if f.count('-') == 2]
        for f in filters:
            prop, op, val = f.split('-')
            if op == 'equal':
                params[prop] = {'$eq': val}
            elif op == 'notEqual':
                params[prop] = {'$ne': val}
            elif op == 'contains':
                params[prop] = {'$regex': val}
            elif op == 'greaterThan':
                params[prop] = {'$gt': val}
            elif op == 'lessThan':
                params[prop] = {'$lt': val}
            elif op == 'isBlank':
                params[prop] = {'$exists': False}
            elif op == 'isPresent':
                params[prop] = {'$exists': True}

        # Other Params
        expand = params.pop('expand', '')
        if 'active' in params:
            params['active'] = params['active'] == 'true'

        count = self.collection.count_documents(params)
        cursor = self.collection.find(params).sort(
            '_id', -1).limit(limit).skip(skip)
        data = [self.Model(**doc).to_json() for doc in cursor]
        data = {
            'object': 'list',
            'url': f'/v1/{self.object}s',
            'has_more': count > len(data),
            'data': data,
            'count': count,
            '_params': params,
        }
        params['expand'] = expand
        return self.expand_data(app, data)

    def create(self, app):

        # Get raw data from request
        data = app.current_event.json_body or {}
        org_header = app.current_event.get_header_value('X-Organization')
        org_body = data.get('organization')
        organization = org_header or org_body

        # Create id if one wasnt included in the request
        oid = data['id'] if data.get('id') else f'{self.prefix}_{ObjectId()}'

        # Add universal fields
        data['_id'] = oid
        data['created'] = int(time.time())
        data['organization'] = organization
        logger.info(data)

        # Add resource specific fields
        data = self.inject_data(data)
        logger.info(data)

        # Convert to Mongo ready item
        data = self.Model(**data)
        logger.info(data)

        # Store in Mongo
        self.collection.insert_one(data.to_bson())

        # Convert to json
        data = data.to_json()
        logger.info(data)

        # Expand fields
        data = self.expand_data(app, data)
        logger.info(data)

        return data

    def get(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization
        found = self.collection.find_one(query)
        if not found:
            raise NotFoundError
        data = self.Model(**found).to_json()
        return self.expand_data(app, data)

    def update(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization
        updates = app.current_event.json_body or {}
        logger.info(updates)
        found = self.get(app, id)
        found.update(updates)
        logger.info(found)
        updated = self.collection.find_one_and_update(
            query,
            {'$set': self.Model(**found).to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        data = self.Model(**updated).to_json()
        return self.expand_data(app, data)

    def tag(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        updates = app.current_event.json_body or {}
        found = self.get(app, id)
        tags = found.get('tags', [])
        for tag in updates.get('tags', []):
            tags.append(tag)
        tags = list(set(tags))
        found.update({'tags': tags})

        query = {'_id': id}
        if organization:
            query['organization'] = organization
        updated = self.collection.find_one_and_update(
            query,
            {'$set': self.Model(**found).to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        data = self.Model(**updated).to_json()
        return self.expand_data(app, data)

    def activate(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization
        found = self.get(app, id)
        found.update({'active': True})
        updated = self.collection.find_one_and_update(
            query,
            {'$set': self.Model(**found).to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        data = self.Model(**updated).to_json()
        return self.expand_data(app, data)

    def archive(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization
        found = self.get(app, id)
        found.update({'active': False})
        updated = self.collection.find_one_and_update(
            query,
            {'$set': self.Model(**found).to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        data = self.Model(**updated).to_json()
        return self.expand_data(app, data)

    def send(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization
        found = self.get(app, id)
        found.update({'status': 'sending'})
        updated = self.collection.find_one_and_update(
            query,
            {'$set': self.Model(**found).to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        data = self.Model(**updated).to_json()
        return self.expand_data(app, data)

    def fulfill(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization

        # Get current data
        data = self.get(app, id)

        # Get raw data from request
        body = app.current_event.json_body or {}
        data.update({
            'wallet_address': body['wallet_address'],
            'status': 'fulfilled'
        })

        # Save updates to Mongo
        data = self.collection.find_one_and_update(
            query,
            {'$set': self.Model(**data).to_bson()},
            return_document=ReturnDocument.AFTER,
        )

        # Convert Mongo item to json
        data = self.Model(**data).to_json()

        # Expand fields
        data = self.expand_data(app, data)
        return data

    def delete(self, app, id):
        organization = app.current_event.get_header_value('X-Organization')
        query = {'_id': id}
        if organization:
            query['organization'] = organization
        deleted = self.collection.find_one_and_delete(query)
        if not deleted:
            raise NotFoundError
        return {
            'id': id,
            'object': self.object,
            'deleted': True
        }

    def aggregate_search(self, app):
        organization = app.current_event.get_header_value('X-Organization')
        params = app.current_event.query_string_parameters or {}
        cursor = self.collection.aggregate([
            Pipeline.search_stage(
                index=self.search_index,
                query=params.get('query')
            ),
            Pipeline.match_stage(
                conditions='',
                match='all',
                org=organization
            )
        ])
        data = [self.Model(**doc).to_json() for doc in cursor]
        return {
            'object': 'search_result',
            'url': f'/v1/{self.object}s/aggregate/search',
            'has_more': False,
            'data': data,
        }

    def aggregate_segment(self, app):
        organization = app.current_event.get_header_value('X-Organization')
        params = app.current_event.query_string_parameters or {}
        type = params.get('type', 'preview')
        vql = params.get('vql', '')
        pipeline = [
            Pipeline.vql_stage(
                vql=vql,
                org=organization
            )
        ]
        count = 0
        data = []
        if type == 'count':
            pipeline.append(Pipeline.count_stage())
            cursor = self.collection.aggregate(pipeline)
            result = json.loads(dumps(list(cursor)))
            if len(result) > 0:
                count = result[0]['count']
        else:
            cursor = self.collection.aggregate(pipeline)
            data = [self.Model(**doc).to_json() for doc in cursor]
        return {
            'object': 'segment_result',
            'url': f'/v1/{self.object}s/aggregate/segment',
            'has_more': False,
            'count': count,
            'data': data,
            'type': type,
            'params': params
        }

    def aggregate_tags(self, app):
        organization = app.current_event.get_header_value('X-Organization')
        cursor = self.collection.aggregate([
            Pipeline.match_stage(org=organization),
            Pipeline.unwind_stage(path='$tags'),
            {
                '$group': {
                    '_id': None,
                    'tags': {
                        '$addToSet': '$tags'
                    }
                }
            }
        ])
        data = json.loads(dumps(list(cursor)))
        tags = []
        if len(data) > 0:
            tags = sorted(data[0]['tags'])
        return {
            'object': 'tags_result',
            'url': f'/v1/{self.object}s/aggregate/tags',
            'has_more': False,
            'data': tags,
        }
