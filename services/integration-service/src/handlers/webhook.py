from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from versify import Versify

from ..utils.api import call_external_api

tracer = Tracer()
logger = Logger()
versify = Versify()


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):

    # Parse event for params
    account = event.detail.get('account')

    # Webhooks are for account events only
    if not account:
        return

    # Save Event to DB
    saved_event = versify.webhook_event_service.create(
        body={
            'account': account,
            'data': {
                'object': event.detail
            },
            'type': event.detail_type
        }
    )

    # Get all matching webhooks this event needs to be sent to
    matching_webhooks = versify.webhook_service.list(
        filter={
            'active': 'true',
            'account': account,
            'enabled_events': event.detail_type
        }
    )

    # Send webhook events
    for webhook in matching_webhooks:
        logger.info('Calling webhook:')
        logger.info(webhook)

        call_external_api(
            method='POST',
            url=webhook['url'],
            account=account,
            body=saved_event
        )

    # TODO: Update Event to DB with the response
    return True
