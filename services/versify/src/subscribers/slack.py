import json
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.slack import send_message

tracer = Tracer()
logger = Logger()

ENV = os.environ.get("ENVIRONMENT", "dev")


def handle_error(message):
    pass


def handle_event(source, detail_type, detail):
    blocks = []

    # Conditionally add divider block
    if ENV == "dev":
        blocks.append(
            {
                "type": "divider",
            }
        )

    # Add event detail type block
    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Event*: {source} -> {detail_type}"
                # "text": f"*Bus*: {bus}\n*Source*: {source}\n*Type*: {detail_type}"
            }
        }
    )

    # Conditionally add detail block
    if ENV == "dev":
        blocks.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"```{json.dumps(detail, indent = 2)}```"
                    }
                ]
            }
        )

    return send_message(blocks)


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    # bus = 'versify' if event.source == 'versify' else 'partner'
    source = event.source
    detail_type = event.detail_type
    detail = event.detail
    if 'user' not in detail_type:
        return handle_event(source, detail_type, detail)
