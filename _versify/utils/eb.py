"""EventBridge utility functions"""
from datetime import datetime

import boto3
import simplejson as json

events = boto3.client('events')
scheduler = boto3.client('scheduler')


def publish_event(detail_type, detail, event_bus, source):
    try:
        eb_event = {
            'DetailType': detail_type,
            'Detail': json.dumps(detail, use_decimal=True),
            'EventBusName': event_bus,
            'Source': source
        }
        events.put_events(Entries=[eb_event])
    except Exception as e:
        print('Error sending event')
        print(e)


def create_rule(name, event_bus, event_pattern=None, schedule_expression=None, enabled=True) -> dict:
    try:
        if event_pattern is not None:
            rule = events.put_rule(
                Name=name,
                EventBusName=event_bus,
                EventPattern=json.dumps(event_pattern),
                State='ENABLED' if enabled else 'DISABLED'
            )
        elif schedule_expression is not None:
            rule = events.put_rule(
                Name=name,
                EventBusName=event_bus,
                ScheduleExpression=schedule_expression,
                State='ENABLED' if enabled else 'DISABLED'
            )
        else:
            raise ValueError('Event pattern or schedule expression required')
        return rule
    except Exception as e:
        print('Error creating rule')
        print(e)
        raise e


def delete_rule(name, event_bus):
    try:
        events.delete_rule(
            Name=name,
            EventBusName=event_bus,
            Force=True
        )
    except Exception as e:
        print('Error deleting rule')
        print(e)
        raise e


def create_schedule(name, expression, target, role, enabled=True, start=None, end=None):
    params = {
        'FlexibleTimeWindow': {
            'MaximumWindowInMinutes': 5,
            'Mode': 'FLEXIBLE'
        },
        'Name': name,
        'ScheduleExpression': expression,
        'State': 'ENABLED' if enabled else 'DISABLED',
        'Target': {
            'Arn': target,
            'RoleArn': role
        }
    }
    if start is not None:
        params['StartDate'] = datetime.fromtimestamp(start)
    if end is not None:
        params['EndDate'] = datetime.fromtimestamp(end)
    try:
        scheduler.create_schedule(**params)
    except Exception as e:
        print('Error creating schedule')
        print(e)
        raise e


def update_schedule(name, expression, target, role, enabled=True, start=None, end=None):
    params = {
        'FlexibleTimeWindow': {
            'MaximumWindowInMinutes': 5,
            'Mode': 'FLEXIBLE'
        },
        'Name': name,
        'ScheduleExpression': expression,
        'State': 'ENABLED' if enabled else 'DISABLED',
        'Target': {
            'Arn': target,
            'RoleArn': role
        }
    }
    if start is not None:
        params['StartDate'] = datetime.fromtimestamp(start)
    if end is not None:
        params['EndDate'] = datetime.fromtimestamp(end)
    try:
        scheduler.update_schedule(**params)
    except Exception as e:
        print('Error updating schedule')
        print(e)
        raise e


def delete_schedule(name):
    try:
        scheduler.delete_schedule(
            Name=name
        )
    except Exception as e:
        print('Error deleting schedule')
        print(e)
        raise e


def create_target(rule, event_bus, target_arn, role_arn) -> dict:
    try:
        target = events.put_targets(
            Rule=rule,
            EventBusName=event_bus,
            Targets=[
                {
                    'Id': rule + '-target',
                    'Arn': target_arn,
                    'RoleArn': role_arn,
                    'InputPath': '$.detail'
                }
            ]
        )
        return target
    except Exception as e:
        print('Error creating target')
        print(e)
        raise e


def remove_targets(rule, event_bus):
    try:
        events.remove_targets(
            Rule=rule,
            EventBusName=event_bus,
            Ids=[rule + '-target']
        )
    except Exception as e:
        print('Error removing targets')
        print(e)
        raise e
