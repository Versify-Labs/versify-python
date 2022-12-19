from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from versify import Versify

tracer = Tracer()
logger = Logger()
versify = Versify()


def handle_collection_deployed(collection):
    logger.info(collection)

    # Create default product for collection
    product_body = {
        'account': collection['account'],
        'active': True,
        'collection': collection['_id'],
        'default': True,
        'image': collection['image'],
    }
    versify.product_service.create(product_body)

    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    collection = event.detail
    event_type = event.detail_type

    if event_type == 'collection.updated' and collection['status'] == 'deployed':
        return handle_collection_deployed(collection)

    return True
