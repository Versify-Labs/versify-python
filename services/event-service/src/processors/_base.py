"""Base class to consume SaaS events and call the appropriate Versify APIs"""
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.logging.logger import Logger
from aws_lambda_powertools.tracing import Tracer

from ..utils.api import call_api

metrics = Metrics()
logger = Logger()
tracer = Tracer()


class BaseProcessor:
    pass

    def __init__(self, api_method, api_path, organization=None) -> None:
        self.api_method = api_method
        self.api_path = api_path
        self.organization = organization

    def extract(self, body):
        return body

    def transform(self, body):
        return body

    def load(self, method, path, body, organization=None):
        api_params = {
            'method': method,
            'path': path,
            'body': body
        }
        if organization:
            api_params['organization'] = organization
        response = call_api(**api_params)
        return response

    def start(self, event):

        event = self.extract(event)
        logger.info(event)

        api_params = self.transform(event)
        logger.info(api_params)

        response = self.load(**api_params)
        logger.info(response)

        return True


class MongoProcessor(BaseProcessor):
    """Consume events from Mongo and call VersifyEventAPI"""

    def transform(self, event):
        doc_key = event.detail['documentKey']
        op_type = event.detail['operationType']
        update_desc = event.detail.get('updateDescription', {})
        update_fields = update_desc.get('updatedFields', {})

        # Get resource type
        resource = doc_key['_id'].split('_')[0]

        # Get action
        action = 'modified'
        try:
            if op_type == 'insert':
                action = 'created'
            elif op_type == 'delete':
                action = 'deleted'
            elif op_type in ['replace', 'update']:
                action = 'updated'
                if 'archived' in update_fields:
                    action = 'archived' if update_fields['archived'] else 'unarchived'
        except:
            action = 'modified'

        # Get data
        if action == 'deleted':
            data = {
                'object': {'id': doc_key}
            }
        else:
            doc = event.detail['fullDocument']
            doc['id'] = doc.pop('_id')
            data = {
                'object': doc
            }

        # Prepare data to send to the EventsAPI
        api_params = {
            'method': 'POST',
            'path': '/internal/events',
            'body':  {
                'data': data,
                'type': f'{resource}.{action}'
            }
        }
        return api_params

    def load(self, detail_type, detail):
        response = publish_event(detail_type, detail, 'versify', 'versify')
        return response
