from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from .service import Versify

tracer = Tracer()
logger = Logger()


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_airdrop_created(event, context):
    airdrop = event.detail
    contact_id = airdrop['contact']
    organization_id = airdrop['organization']
    versify = Versify(organization_id)
    versify.contacts.add_airdrop(contact_id)
    return True


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_order_created(event, context):
    organization = event.detail['organization']
    versify = Versify(organization)
    versify.contacts.update_with_order(order=event.detail)
    return True
