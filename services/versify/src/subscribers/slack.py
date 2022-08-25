import json

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.slack import send_message

tracer = Tracer()
logger = Logger()


def handle_error(message):
    pass


def handle_event(source, detail_type):
    blocks = [
        # {
        #     "type": "divider"
        # },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Event*: {source} -> {detail_type}"
                # "text": f"*Bus*: {bus}\n*Source*: {source}\n*Type*: {detail_type}"
            }
        },
        # {
        #     "type": "context",
        #     "elements": [
        #         {
        #             "type": "mrkdwn",
        #             "text": f"```{json.dumps(detail, indent = 2)}```"
        #         }
        #     ]
        # }
    ]
    return send_message(blocks)


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    # bus = 'versify' if event.source == 'versify' else 'partner'
    source = event.source
    detail_type = event.detail_type
    # detail = event.detail
    return handle_event(source, detail_type)
