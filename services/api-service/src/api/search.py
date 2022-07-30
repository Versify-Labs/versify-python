from enum import Enum

import simplejson as json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from bson.json_util import dumps

from ..utils.mongo import mdb
from .config import config
from .errors import BadRequestError
from .pipelines import (count_stage, group_stage, match_stage, search_stage,
                        unwind_stage, vql_stage)

logger = Logger()


class SearchType(Enum):
    """An enumerations of the supported search types."""

    AggregateTags = "aggregate_tags"
    CountSegmentContacts = "count_segment_contacts"
    ListSegmentContacts = "list_segment_contacts"
    SearchContacts = "search_contacts"
    SearchProducts = "search_products"
    UsageStats = 'usage_stats'


class Search:

    def __init__(self, app: APIGatewayRestResolver):

        query_params = app.current_event.query_string_parameters or {}

        # Parse request for params
        self._search_type = query_params.get('search_type')
        self._account = app.current_event.get_header_value('Versify-Account')
        self._query = query_params.get('query', '')
        self._vql = query_params.get('vql', '')
        self._url = app.current_event.path

    def get_collection(self, resource):
        cfg = config[resource]
        return mdb[cfg.db][cfg.collection]

    def get_index(self, resource):
        return config[resource].search_index

    def get_model(self, resource):
        return config[resource].model

    def aggregate_tags(self):
        collection = self.get_collection('contact')
        stages = [
            match_stage(account=self._account),
            unwind_stage(path='$tags'),
            group_stage(field='tags')
        ]
        cursor = collection.aggregate(stages)
        data = json.loads(dumps(list(cursor)))
        tags = []
        if len(data) > 0:
            tags = sorted(data[0]['tags'])
        return tags

    def count_segment_contacts(self):
        collection = self.get_collection('contact')
        stages = [
            vql_stage(vql=self._vql, account=self._account),
            count_stage()
        ]
        cursor = collection.aggregate(stages)
        result = json.loads(dumps(list(cursor)))
        return result[0]['count']

    def list_segment_contacts(self):
        collection = self.get_collection('contact')
        model = self.get_model('contact')
        stages = [
            vql_stage(vql=self._vql, account=self._account)
        ]
        cursor = collection.aggregate(stages)
        return [model(**doc).to_json() for doc in cursor]

    def search_contacts(self):
        collection = self.get_collection('contact')
        model = self.get_model('contact')
        index = self.get_index('contact')
        stages = [
            search_stage(index=index, query=self._query),
            match_stage(
                conditions='',
                match='all',
                account=self._account
            )
        ]
        cursor = collection.aggregate(stages)
        return [model(**doc).to_json() for doc in cursor]

    def search_products(self):
        collection = self.get_collection('product')
        model = self.get_model('product')
        index = self.get_index('product')
        stages = [
            search_stage(index=index, query=self._query),
            match_stage(
                conditions='',
                match='all',
                account=self._account
            )
        ]
        cursor = collection.aggregate(stages)
        return [model(**doc).to_json() for doc in cursor]

    def usage_stats(self):
        # TODO: Implement
        # collection = self.get_collection('mint')
        # stages = [
        #     vql_stage(vql=self._vql, account=self._account),
        #     count_stage()
        # ]
        # cursor = collection.aggregate(stages)
        # result = json.loads(dumps(list(cursor)))
        # return result[0]['count']
        return []

    def run(self):
        data = None
        logger.info(self._search_type)
        logger.info(SearchType.SearchContacts)

        if self._search_type == SearchType.AggregateTags.value:
            data = self.aggregate_tags()
        elif self._search_type == SearchType.CountSegmentContacts.value:
            data = self.count_segment_contacts()
        elif self._search_type == SearchType.ListSegmentContacts.value:
            data = self.list_segment_contacts()
        elif self._search_type == SearchType.SearchContacts.value:
            data = self.search_contacts()
        elif self._search_type == SearchType.SearchProducts.value:
            data = self.search_products()
        elif self._search_type == SearchType.UsageStats.value:
            data = self.usage_stats()
        else:
            e = f"'{self._search_type}' is not a valid Search Type"
            raise BadRequestError(e)

        return {
            'object': 'search',
            'url': self._url,
            'has_more': False,
            'data': data
        }
