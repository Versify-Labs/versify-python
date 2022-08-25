from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..services import CollectionService, ContactService

tracer = Tracer()
logger = Logger()
collection_service = CollectionService()
contact_service = ContactService()


def handle_account_created(account):
    logger.info(account)

    # Create default collection
    collection_body = {
        'account': account['id'],
        'default': True,
        'name': account['business_profile']['name']
    }
    collection_service.create(collection_body)

    # Create default contact
    contact_body = {
        'account': account['id'],
        'email': account['email'],
        'tags': ['Team']
    }
    contact_service.create(contact_body)

    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    account = event.detail
    event_type = event.detail_type

    if event_type == 'account.created':
        return handle_account_created(account)

    return True
