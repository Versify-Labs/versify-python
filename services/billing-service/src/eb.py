import os
import re
from datetime import datetime

import boto3
import simplejson as json
import urllib3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters
from boto3.dynamodb.types import TypeDeserializer

EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']

events = boto3.client('events')


def publish_event(detail_type, detail, source='versify', resources=[], timestamp=None):
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
