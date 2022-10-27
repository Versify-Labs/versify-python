from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..services import AccountService, ContactService, UserService

tracer = Tracer()
logger = Logger()
account_service = AccountService()
contact_service = ContactService()
user_service = UserService(account_service)


def sync_contact_user(contact):
    logger.info(contact)

    # See if a user exists for this contact
    user = user_service.retrieve_by_email(contact['email'])

    # If the user doesn't exist, create it
    if not user:
        new_user = {'email': contact['email']}
        user = user_service.create(new_user)
        logger.info(user)

    return True


def handle_contact_created(contact):
    return sync_contact_user(contact)


def handle_contact_updated(contact):
    return sync_contact_user(contact)


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
