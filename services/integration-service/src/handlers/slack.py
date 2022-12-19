from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.slack import send_message

tracer = Tracer()
logger = Logger()


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    """Consume events from EventBus and publish to Slack"""
    source = event.source
    detail_type = event.detail_type
    text = f"*Event*: {source} -> {detail_type}"
    return send_message(text=text)
