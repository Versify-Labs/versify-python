from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (DynamoDBStreamEvent,
                                                          EventBridgeEvent,
                                                          event_source)

from .service import EventService

tracer = Tracer()
logger = Logger()


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def publish_dynamo_event(event, context):
    event = DynamoDBStreamEvent(event)
    service = EventService()
    return service.process_stream(event.records)


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_method
def send_slack_message(event, context):
    source = event.source
    detail_type = event.detail_type
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Event*: {source} -> {detail_type}"
            }
        }
    ]
    service = EventService()
    return service.post_slack_message(blocks)
