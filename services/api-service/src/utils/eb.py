"""EventBridge utility functions"""

import boto3
import simplejson as json

events = boto3.client("events")


def publish_event(detail_type, detail, event_bus, source):
    try:
        eb_event = {
            "DetailType": detail_type,
            "Detail": json.dumps(detail, use_decimal=True),
            "EventBusName": event_bus,
            "Source": source,
        }
        events.put_events(Entries=[eb_event])
    except Exception as e:
        print("Error sending event")
        print(e)
