import time

from versify import Versify

versify = Versify()


def execution_to_run_result(execution):
    return {
        'execution_id': execution['id'],
        'state_name': execution['state_name'],
        'status': execution['status'],
        'time_started': execution['time_started'],
        'time_ended': execution['time_ended'],
        'result': execution['result'],
    }


def create_run(event):
    print('Creating run')

    # Parse event for parameters
    journey_id = event.get('journey_id', None)
    trigger_event = event.get('trigger_event', None)

    # Create run
    run = versify.journey_run_service.create(body={
        'account': trigger_event['account'],
        'contact': trigger_event['contact'],
        'journey': journey_id,
        'results': [],
        'status': 'running',
        'time_started': int(time.time()),
        'trigger_event': trigger_event
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': run['id'],
    }


def update_run(event):
    print('Updating run')

    # Parse event for parameters
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)
    status = event.get('status', None)

    # Update run
    versify.journey_run_service.update(
        id=journey_run_id,
        body={
            'status': status,
            'time_ended': int(time.time())
        }
    )

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id,
    }
