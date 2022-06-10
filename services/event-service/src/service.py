import os
import re
from datetime import datetime

import boto3
import simplejson as json
import urllib3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters
from boto3.dynamodb.types import TypeDeserializer

tracer = Tracer()
logger = Logger()
events = boto3.client('events')

EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']
GENESIS_ADDRESS = '0x0000000000000000000000000000000000000000'
SECRET = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET)
SLACK_CHANNEL = SECRET['SLACK_CHANNEL_ID']
SLACK_TOKEN = SECRET['SLACK_API_TOKEN']


class EventService:

    def __init__(self):
        pass

    def get_event_type(self, table_arn, detail, event_name):
        action_map = {
            'INSERT': 'created',
            'MODIFY': 'updated',
            'REMOVE': 'deleted'
        }
        object_map = {
            'BlockchainServiceTable': {
                'signature': 'signature',
                'transaction': 'transaction'
            },
            'CampaignServiceTable': {
                'airdrop': 'airdrop',
                'campaign': 'campaign'
            },
            'CrmServiceTable': {
                'contact': 'contact',
                'activity': 'contact.activity',
                'note': 'contact.note',
                'tag': 'tag',
            },
            'PimServiceTable': {
                'collection': 'collection',
                'product': 'product',
            },
            'WalletServiceTable': {
                'account': 'account'
            }
        }
        table_name = table_arn.split('/')[-1]

        # Get resource
        resource = 'resource'

        if event_name in ['INSERT', 'MODIFY']:
            object = detail['object']
        elif event_name == 'REMOVE' and 'Wallet' in table_name and 'did' in detail['id']:
            object = 'account'
        elif event_name == 'REMOVE':
            try:
                object = detail.get('id').split('_')[0]
            except:
                object = 'object'
        else:
            object = 'object'
        try:
            resource = object_map[table_name][object]
        except:
            resource = 'resource'
        resource = re.sub(r'(?<!^)(?=[A-Z])', '_', resource).lower()

        # Get action
        action = action_map[event_name]

        return f'{resource}.{action}'

    def publish_event(self, detail_type, detail, source='versify', resources=[], timestamp=None):
        try:
            eb_event = {
                'DetailType': detail_type,
                'Detail': json.dumps(detail, use_decimal=True),
                'EventBusName': EVENT_BUS_NAME,
                'Resources': resources,
                'Source': source
            }
            if timestamp:
                eb_event['Time'] = timestamp
            events.put_events(Entries=[eb_event])
        except Exception as e:
            print('Error sending event')
            print(e)

    def process_auth_events(self, logs):
        code_map = {
            's': 'Successful login',
            'scoa': 'Successful cross-origin authentication',
            'sens': 'Successful native social login',
            'w': 'Warnings during login',
            'f': 'Failed login',
            'flo': 'User logout failure',
            'fs': 'User signup failure',
            'ss': 'User signup success',
            'slo': 'User logout success',
            'fco': 'Origin is not in the applications Allowed Origins list',
            'fp': 'Incorrect password',
            'fu': 'Invalid email/username',
        }
        source = 'auth0'
        for log in logs:
            code = log['data']['type']
            if code in code_map:
                detail_type = code_map[code]
            else:
                detail_type = log['data'].get('description', 'auth.event')
            detail = log['data']
            self.publish_event(detail_type, detail, source)
        return True

    def process_blockchain_events(self, activities):
        source = 'alchemy'
        detail_type = 'address.activity'
        for activity in activities:
            detail = activity
            self.publish_event(detail_type, detail, source)
        return True

    def process_stream(self, records):
        deserializer = TypeDeserializer()
        for record in records:
            event_name = record['eventName']
            if event_name in ['INSERT', 'MODIFY']:
                dynamo_item = record['dynamodb']['NewImage']
            else:
                dynamo_item = record['dynamodb']['Keys']
            table_arn, _ = record['eventSourceARN'].split('/stream')
            detail = {k: deserializer.deserialize(
                v) for k, v in dynamo_item.items()}
            detail_type = self.get_event_type(table_arn, detail, event_name)
            source = 'versify'
            resources = [table_arn]
            timestamp = datetime.utcfromtimestamp(
                record['dynamodb']['ApproximateCreationDateTime']
            )
            self.publish_event(detail_type, detail, source,
                               resources, timestamp)
        return True

    def post_slack_message(self, blocks=[], text='', channel=SLACK_CHANNEL):
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
