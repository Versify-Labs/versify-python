"""Base class to consume SaaS events and call the appropriate Versify APIs"""
import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.logging.logger import Logger
from aws_lambda_powertools.tracing import Tracer

from ..utils.eb import publish_event

events = boto3.client('events')
metrics = Metrics()
logger = Logger()
tracer = Tracer()


class BasePublisher:
    pass

    def __init__(self):
        pass

    def extract(self, event):
        return event

    def transform(self, event):
        # Prepare data to send to EventBridge
        event_params = {
            'detail_type': 'event.created',
            'detail': event.detail['fullDocument']
        }
        return event_params

    def load(self, detail_type, detail):
        response = publish_event(detail_type, detail, 'versify', 'versify')
        return response

    def start(self, event):

        event = self.extract(event)
        logger.info(event)

        event_params = self.transform(event)
        logger.info(event_params)

        response = self.load(**event_params)
        logger.info(response)

        return response
