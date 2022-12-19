from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from versify import Versify

tracer = Tracer()
logger = Logger()
versify = Versify()


def handle_contact_created(contact):
    user = versify.user_service.get(contact['email'])
    return user


def handle_contact_updated(contact):
    user = versify.user_service.get(contact['email'])
    return user


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    contact = event.detail
    event_type = event.detail_type

    if event_type == 'contact.created':
        return handle_contact_created(contact)
    if event_type == 'contact.updated':
        return handle_contact_updated(contact)

    return True
