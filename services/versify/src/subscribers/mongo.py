
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.eb import publish_event

tracer = Tracer()
logger = Logger()


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    """Consume events from Mongo and publish to the PartnerBus"""
    detail_type = event.detail_type
    detail = event.detail
    event_bus = 'partner'
    source = 'mongo'
    publish_event(detail_type, detail, event_bus, source)
    return True
