import simplejson as json
import urllib3

from ..config import SlackConfig


def send_message(blocks=[], text="", channel=None):
    if not channel:
        channel = SlackConfig.SLACK_CHANNEL

    data = {"channel": channel, "blocks": blocks, "text": text}
    http = urllib3.PoolManager()
    resp = http.request(
        method="POST",
        url="https://slack.com/api/chat.postMessage",
        body=json.dumps(data),
        headers={
            "Authorization": f"Bearer {SlackConfig.SLACK_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    return resp.data
