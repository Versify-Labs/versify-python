import json

from ..utils.slack import send_message
from ._base import BaseSubscriber


class SlackSubscriber(BaseSubscriber):

    def start(self, event):
        bus = 'versify' if event.source == 'versify' else 'partner'
        source = event.source
        detail_type = event.detail_type
        detail = event.detail
        blocks = [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    # "text": f"*Event*: {source} -> {detail_type}"
                    "text": f"*Bus*: {bus}\n*Source*: {source}\n*Type*: {detail_type}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"```{json.dumps(detail, indent = 2)}```"
                    }
                ]
            }
        ]
        return send_message(blocks)
