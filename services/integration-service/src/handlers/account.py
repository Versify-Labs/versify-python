from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from versify import Versify

tracer = Tracer()
logger = Logger()
versify = Versify()


def handle_account_created(account):
    logger.info(account)

    # Create default collection
    collection_body = {
        'account': account['_id'],
        'default': True,
        'name': account['name']
    }
    versify.collection_service.create(collection_body)

    # Create default contact
    contact_body = {
        'account': account['_id'],
        'email': account['email'],
        'tags': ['Team']
    }
    versify.contact_service.create(contact_body)

    return True


def handle_account_updated(account):
    logger.info(account)
    return True


def handle_account_deleted(account):
    logger.info(account)
    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    account = event.detail
    event_type = event.detail_type

    if event_type == 'account.created':
        return handle_account_created(account)
    if event_type == 'account.updated':
        return handle_account_updated(account)
    if event_type == 'account.deleted':
        return handle_account_deleted(account)

    return True
