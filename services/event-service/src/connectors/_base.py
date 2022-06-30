"""Base class to consume SaaS events and publish to the PartnerBus"""
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.logging.logger import Logger
from aws_lambda_powertools.tracing import Tracer

from ..utils.eb import publish_event

metrics = Metrics()
logger = Logger()
tracer = Tracer()


class BaseConnector:

    def __init__(self, source) -> None:
        self.source = source

    def extract(self, event):
        return event

    def transform(self, body):
        return body

    def load(self, detail_type, detail):
        response = publish_event(detail_type, detail, 'partner', self.source)
        return response

    def start(self, event):

        event = self.extract(event)
        logger.info(event)

        event_params = self.transform(event)
        logger.info(event_params)

        response = self.load(**event_params)
        logger.info(response)

        return True


class MongoConnector(BaseConnector):
    """Consume events from Mongo and publish to the PartnerBus"""

    def __init__(self) -> None:
        super().__init__('mongo')

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

        # Prepare data to send to the PartnerBus
        event_params = {
            'detail_type': 'MongoEvent',
            'detail': data
        }
        return event_params
