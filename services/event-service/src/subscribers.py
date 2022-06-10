import json
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (DynamoDBStreamEvent,
                                                          EventBridgeEvent,
                                                          event_source)

from .service import EventService

tracer = Tracer()
logger = Logger()


# @event_source(data_class=EventBridgeEvent)
# @logger.inject_lambda_context(log_event=True)
# @tracer.capture_lambda_handler
# def create_event(event, context):
#     detail_type = event.detail_type
#     detail = event.detail
#     source = event.source
#     service = EventService()
#     return service.save_event(detail_type, detail, source)


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
    # detail = event.detail
    blocks = [
        # {
        #     "type": "divider"
        # },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Event*: {source} -> {detail_type}"
            }
        }
    ]
    # if os.environ.get('ENVIRONMENT', 'dev') == 'dev':
    #     blocks.append(
    #         {
    #             "type": "context",
    #             "elements": [
    #                 {
    #                     "type": "mrkdwn",
    #                     "text": f"```{json.dumps(detail, indent = 2)}```"
    #                 }
    #             ]
    #         }
    #     )
    service = EventService()
    return service.post_slack_message(blocks)
