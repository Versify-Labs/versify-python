"""StepFunction utility functions"""
import boto3
import simplejson as json
from botocore.exceptions import ClientError

sfn = boto3.client('stepfunctions')


def create_state_machine(name, definition, role_arn, log_arn):
    try:
        state_machine = sfn.create_state_machine(
            name=name,
            definition=json.dumps(definition),
            roleArn=role_arn,
            type='STANDARD',
            loggingConfiguration={
                'level': 'ALL',
                'includeExecutionData': True,
                'destinations': [
                    {
                        'cloudWatchLogsLogGroup': {
                            'logGroupArn': log_arn
                        }
                    },
                ]
            },
            tracingConfiguration={
                'enabled': True
            },
        )
        return state_machine
    except ClientError as e:
        print('Error creating state machine')
        print(e)
        raise e


def update_state_machine(arn, definition, role_arn):
    try:
        state_machine = sfn.update_state_machine(
            stateMachineArn=arn,
            definition=json.dumps(definition),
            roleArn=role_arn
        )
        return state_machine
    except ClientError as e:
        print('Error updating state machine')
        print(e)
        raise e


def delete_state_machine(arn):
    try:
        sfn.delete_state_machine(
            stateMachineArn=arn
        )
    except ClientError as e:
        print('Error deleting state machine')
        print(e)
        raise e


def start_execution(state_machine_arn, input):
    try:
        execution = sfn.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input)
        )
        return execution
    except ClientError as e:
        print('Error starting execution')
        print(e)
        raise e


def list_executions(state_machine_arn, status_filter=None):
    try:
        executions = sfn.list_executions(
            stateMachineArn=state_machine_arn,
            statusFilter=status_filter
        )
        return executions
    except ClientError as e:
        print('Error listing executions')
        print(e)
        raise e
