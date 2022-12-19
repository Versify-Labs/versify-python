import os

import simplejson as json
import urllib3
from aws_lambda_powertools.utilities import parameters

SECRET = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET)
SLACK_CHANNEL = SECRET['SLACK_CHANNEL_ID']
SLACK_TOKEN = SECRET['SLACK_API_TOKEN']


def send_message(blocks=[], text='', channel=SLACK_CHANNEL):
    data = {
        "channel": channel,
        "blocks": blocks,
        "text":  text
    }
    http = urllib3.PoolManager()
    resp = http.request(
        method='POST',
        url='https://slack.com/api/chat.postMessage',
        body=json.dumps(data),
        headers={
            'Authorization': f'Bearer {SLACK_TOKEN}',
            "Content-Type": "application/json"
        }
    )
    return resp.data
