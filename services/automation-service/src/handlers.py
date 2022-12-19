import json
import time

from versify import Versify

versify = Versify()


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
        'results': {},
        'status': 'running',
        'time_started': int(time.time()),
        'trigger_event': trigger_event
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': run['id']
    }


def update_run(event):
    print('Updating run')

    # Parse event for parameters
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)
    status = event.get('status', None)

    # Update the run's results
    update_body = {
        'status': status,
        'time_ended': int(time.time()),
    }
    versify.journey_run_service.update(
        id=journey_run_id,
        body=update_body
    )

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id
    }


def update_run_state_results(run_id, state_name, state_result):

    # Get the run
    run = versify.journey_run_service.retrieve_by_id(run_id)

    # Update the run's results
    results = run.get('results', {})
    results[state_name] = {
        'name': state_name,
        'result': state_result,
        'status': 'completed',
        'time_started': int(time.time()),
        'time_ended': int(time.time()),
    }
    versify.journey_run_service.update(
        id=run_id,
        body={
            'results': results
        }
    )

    return True


def match_all_filters(contact, filters):
    match = True

    # Check if all filters are met
    for criterion in filters:
        field = criterion['field']
        operator = criterion['operator']
        value = criterion['value']

        # Get the contact's value for the field
        contact_value = contact.get(field, None)

        # Check if the contact's value matches the criterion
        if operator == 'equal':
            if contact_value != value:
                match = False
                break
        elif operator == 'not_equal':
            if contact_value == value:
                match = False
                break
        elif operator == 'exists':
            if not contact_value:
                match = False
                break
        elif operator == 'not_exists':
            if contact_value:
                match = False
                break
        elif operator == 'starts_with':
            if not contact_value.startswith(value):
                match = False
                break
        elif operator == 'not_starts_with':
            if contact_value.startswith(value):
                match = False
                break
        elif operator == 'ends_with':
            if not contact_value.endswith(value):
                match = False
                break
        elif operator == 'not_ends_with':
            if contact_value.endswith(value):
                match = False
                break
        elif operator == 'greater_than':
            if contact_value <= value:
                match = False
                break
        elif operator == 'greater_than_or_equal':
            if contact_value < value:
                match = False
                break
        elif operator == 'less_than':
            if contact_value >= value:
                match = False
                break
        elif operator == 'less_than_or_equal':
            if contact_value > value:
                match = False
                break
        else:
            raise Exception('Invalid operator')

    return match


def match_any_filters(contact, filters):
    match = False

    # Check if any filters are met
    for criterion in filters:
        field = criterion['field']
        operator = criterion['operator']
        value = criterion['value']

        # Get the contact's value for the field
        contact_value = contact.get(field, None)

        # Check if the contact's value matches the criterion
        if operator == 'equal':
            if contact_value == value:
                match = True
                break
        elif operator == 'not_equal':
            if contact_value != value:
                match = True
                break
        elif operator == 'exists':
            if contact_value:
                match = True
                break
        elif operator == 'not_exists':
            if not contact_value:
                match = True
                break
        elif operator == 'starts_with':
            if contact_value.startswith(value):
                match = True
                break
        elif operator == 'not_starts_with':
            if not contact_value.startswith(value):
                match = True
                break
        elif operator == 'ends_with':
            if contact_value.endswith(value):
                match = True
                break
        elif operator == 'not_ends_with':
            if not contact_value.endswith(value):
                match = True
                break
        elif operator == 'greater_than':
            if contact_value > value:
                match = True
                break
        elif operator == 'greater_than_or_equal':
            if contact_value >= value:
                match = True
                break
        elif operator == 'less_than':
            if contact_value < value:
                match = True
                break
        elif operator == 'less_than_or_equal':
            if contact_value <= value:
                match = True
                break
        else:
            raise Exception('Invalid operator')

    return match


def match(event, all_filters=False):
    print('Checking filters against contact')

    # Parse event for parameters
    state_name = event.get('state_name', None)
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)

    # Get contact data
    journey = versify.journey_service.get(journey_id)
    journey_run = versify.journey_run_service.retrieve_by_id(journey_run_id)
    contact = versify.contact_service.get(journey_run['contact'])

    # Get the state config
    state = journey['states'][state_name]
    config = state['config']
    filters = config['filters']

    # Check if filters is met
    if all_filters:
        match = match_all_filters(contact, filters)
    else:
        match = match_any_filters(contact, filters)

    # Update results
    update_run_state_results(journey_run_id, state_name, {
        'filters': filters,
        'match': match
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id,
        'match': match
    }


def create_note(event):
    print('Creating note')

    # Parse event for parameters
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)
    state_name = event.get('state_name', None)

    # Get contact data
    journey = versify.journey_service.get(journey_id)
    journey_run = versify.journey_run_service.retrieve_by_id(journey_run_id)
    contact = versify.contact_service.get(journey_run['contact'])

    # Get the state config
    state = journey['states'][state_name]
    config = state['config']
    note = config['note']

    # Create note
    note = versify.note_service.create(body={
        'account': journey['account'],
        'contact': contact['id'],
        'content': note,
        'resource_id': contact['id'],
        'resource_type': 'contact',
        'user': {
            'id': 'system',
        }
    })

    # Update run
    update_run_state_results(journey_run_id, state_name, {
        'note_id': note['id']
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id
    }


def send_message(event):
    print('Sending message')

    # Parse event for parameters
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)
    state_name = event.get('state_name', None)

    # Get contact data
    journey = versify.journey_service.get(journey_id)
    journey_run = versify.journey_run_service.retrieve_by_id(journey_run_id)
    contact = versify.contact_service.get(journey_run['contact'])
    if not contact:
        raise Exception('Contact not found')

    # Get the state config
    state = journey['states'][state_name]
    config = state['config']

    # Create and send message
    message = versify.message_service.create(
        body={
            'account': journey['account'],
            'type': config['type'],
            'content_body': config.get('body'),
            'content_subject': config.get('subject'),
            'from_email': config['from_email'],
            'to_contact': contact['id'],
            'to_email': contact['email'],
            'to_name': contact.get('name', contact['email']),
        }
    )
    message = versify.message_service.send(message['id'])

    # Update results
    update_run_state_results(journey_run_id, state_name, {
        'message_id': message['id'],
        'message_status': message['status'],
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id
    }


def send_reward(event):
    print('Sending reward')

    # Parse event for parameters
    state_name = event.get('state_name', None)
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)

    # Get contact data
    journey = versify.journey_service.get(journey_id)
    journey_run = versify.journey_run_service.retrieve_by_id(journey_run_id)
    contact = versify.contact_service.get(journey_run['contact'])
    if not contact:
        raise Exception('Contact not found')
    product = journey['states'][state_name]['config']['product']

    # Create mint
    mint = versify.mint_service.create(body={
        'account': journey_run['account'],
        'contact': contact['id'],
        'email': contact['email'],
        'journey': journey_id,
        'journey_run': journey_run_id,
        'product': product
    })

    # Update the results
    update_run_state_results(journey_run_id, state_name, {
        'mint_id': mint['id'],
        'mint_status': mint['status'],
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id
    }


def tag_contact(event):
    print('Tagging contact')

    # Parse event for parameters
    journey_id = event.get('journey_id', None)
    journey_run_id = event.get('journey_run_id', None)
    state_name = event.get('state_name', None)

    # Get contact data
    journey = versify.journey_service.get(journey_id)
    journey_run = versify.journey_run_service.retrieve_by_id(journey_run_id)
    contact = versify.contact_service.get(journey_run['contact'])
    if not contact:
        raise Exception('Contact not found')
    old_tags = contact.get('tags', [])

    # Get the state config
    state = journey['states'][state_name]
    config = state['config']
    tags = config['tags']

    # Tag contact
    new_tags = old_tags + tags
    versify.contact_service.update(contact['id'], body={
        'tags': new_tags
    })

    # Update results
    update_run_state_results(journey_run_id, state_name, {
        'tags': new_tags
    })

    return {
        'journey_id': journey_id,
        'journey_run_id': journey_run_id
    }


def handler(event, context):
    print('Event:')
    print(json.dumps(event, indent=2))
    task_type = event.get('task_type', None)

    if task_type == 'create_run':
        return create_run(event)
    elif task_type == 'match_all':
        return match(event, all_filters=True)
    elif task_type == 'match_any':
        return match(event, all_filters=False)
    elif task_type == 'create_note':
        return create_note(event)
    elif task_type == 'send_app_message':
        return send_message(event)
    elif task_type == 'send_email_message':
        return send_message(event)
    elif task_type == 'send_reward':
        return send_reward(event)
    elif task_type == 'tag_contact':
        return tag_contact(event)
    elif task_type == 'update_run':
        return update_run(event)
    else:
        print(f'Unknown task type: {task_type}')
        return {}
