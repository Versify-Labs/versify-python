import time
from datetime import datetime

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import Config, JourneyConfig
from ..utils.eb import (create_rule, create_schedule, create_target,
                        delete_rule, delete_schedule, remove_targets,
                        update_schedule)
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.mongo import mdb
from ..utils.sfn import (create_state_machine, delete_state_machine,
                         update_state_machine)


class JourneyService(ExpandableResource):

    def __init__(self) -> None:
        self.collection = mdb[JourneyConfig.db][JourneyConfig.collection]
        self.expandables = JourneyConfig.expandables
        self.Model = JourneyConfig.model
        self.object = JourneyConfig.object
        self.prefix = JourneyConfig.prefix
        self.search_index = JourneyConfig.search_index

    def journey_to_event_pattern(self, journey: dict) -> dict:
        """Create the event pattern for a journey trigger.

        Args:
            journey (dict): The journey to create the event pattern for.

        Returns:
            dict: The event pattern.
        """

        # Parse trigger config
        trigger_config = journey['trigger']['config']
        trigger_schedule = trigger_config.get('schedule')
        trigger_source = trigger_config['source']
        trigger_detail_type = trigger_config['detail_type']
        trigger_detail_filters = trigger_config.get('detail_filters')

        # Create event pattern
        event_pattern = {
            'source': ['versify'],
            'detail-type': ['event.created'],
            'detail': {
                'account': [journey['account']],
                'source': [trigger_source],
                'detail_type': [trigger_detail_type]
            }
        }

        # Add schedule to event pattern
        if trigger_schedule and trigger_schedule != {}:
            schedule_start = trigger_schedule.get('start', None)
            schedule_end = trigger_schedule.get('end', None)
            created_filter = {'numeric': []}
            if schedule_start:
                created_filter['numeric'].append('>=')
                created_filter['numeric'].append(schedule_start)
            if schedule_end:
                created_filter['numeric'].append('<=')
                created_filter['numeric'].append(schedule_end)
            event_pattern['detail']['created'] = [created_filter]

        # Add detail filters to event pattern
        if trigger_detail_filters and trigger_detail_filters != {}:
            detail_pattern = {}
            for filter in trigger_detail_filters:
                filter_field = filter['field']
                filter_operator = filter['operator']
                filter_value = filter['value']
                pattern = []
                if filter_operator == 'equal':
                    pattern = [filter_value]
                elif filter_operator == 'not_equal':
                    pattern = [{'anything-but': [filter_value]}]
                elif filter_operator == 'exists':
                    pattern = [{'exists': True}]
                elif filter_operator == 'not_exists':
                    pattern = [{'exists': False}]
                elif filter_operator == 'starts_with':
                    pattern = [{'prefix': filter_value}]
                elif filter_operator == 'not_starts_with':
                    pattern = [{'anything-but': [{'prefix': filter_value}]}]
                elif filter_operator == 'ends_with':
                    pattern = [{'suffix': filter_value}]
                elif filter_operator == 'not_ends_with':
                    pattern = [{'anything-but': [{'suffix': filter_value}]}]
                elif filter_operator == 'greater_than':
                    pattern = [{'numeric': ['>', filter_value]}]
                elif filter_operator == 'greater_than_or_equal':
                    pattern = [{'numeric': ['>=', filter_value]}]
                elif filter_operator == 'less_than':
                    pattern = [{'numeric': ['<', filter_value]}]
                elif filter_operator == 'less_than_or_equal':
                    pattern = [{'numeric': ['<=', filter_value]}]
                else:
                    raise Exception('Invalid filter operator')
                detail_pattern[filter_field] = pattern
            event_pattern['detail']['detail'] = detail_pattern

        return event_pattern

    def journey_to_schedule(self, journey: dict) -> tuple:
        """Create the schedule expression for a journey trigger.

        Args:
            journey (dict): The journey to create the schedule expression for.

        Returns:
            str: The schedule expression.
        """

        # Parse trigger config
        trigger_config = journey['trigger']['config']
        trigger_schedule = trigger_config.get('schedule', {})
        trigger_schedule_at = trigger_schedule.get('at', None)
        trigger_schedule_cron = trigger_schedule.get('cron', None)
        trigger_schedule_rate = trigger_schedule.get('rate', None)
        trigger_schedule_start = trigger_schedule.get('start', None)
        trigger_schedule_end = trigger_schedule.get('end', None)

        # Create schedule parameters
        start_date = None
        end_date = None

        if trigger_schedule_at:
            schedule_at = int(trigger_schedule_at)
            schedule_at = datetime.fromtimestamp(schedule_at)
            schedule_at = schedule_at.strftime('%Y-%m-%dT%H:%M:%S')
            expression = f'at({schedule_at})'
        elif trigger_schedule_cron:
            expression = f'cron({trigger_schedule_cron})'
        elif trigger_schedule_rate:
            expression = f'rate({trigger_schedule_rate})'
        else:
            raise Exception('Invalid schedule')

        if trigger_schedule_start:
            start_date = trigger_schedule_start
        if trigger_schedule_end:
            end_date = trigger_schedule_end

        return expression, start_date, end_date

    def journey_to_definition(self, journey: dict) -> dict:
        """Convert states to step function definition

        Args:
            states (dict): The states to convert

        Returns:
            dict: The step function definition
        """
        journey_id = journey['id']
        start = journey['start']
        states = journey['states']

        definition = {
            'Comment': 'Workflow for Versify Journeys',
            'StartAt': 'Create run',
            'States': {}
        }

        # Insert create run state
        definition['States']['Create run'] = {
            'Type': 'Task',
            'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
            'InputPath': '$',
            'Parameters': {
                'state_name.$': '$$.State.Name',
                'task_type': 'create_run',
                'journey_id': journey_id,
                'trigger_event.$': '$'
            },
            'OutputPath': '$',
            'Next': 'Start run'
        }

        # Insert start state
        definition['States']['Start run'] = {
            'Type': 'Wait',
            'Seconds': 3,
            'Next': start
        }

        failure_prone = False

        # Insert user generated states
        for name, versify_definition in states.items():
            action_type = versify_definition['type'].lower()

            # Check if current state is the last state
            if versify_definition.get('end', False):
                next_state = 'Save success run'
            else:
                next_state = versify_definition.get('next', None)

            if action_type == 'create_note':
                definition['States'][name] = {
                    'Type': 'Task',
                    'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                    'InputPath': '$',
                    'Parameters': {
                        'state_name.$': '$$.State.Name',
                        'task_type': action_type,
                        'journey_id': journey_id,
                        'journey_run_id.$': '$.journey_run_id'
                    },
                    'OutputPath': '$',
                    'Catch': [
                        {
                            'ErrorEquals': ['States.ALL'],
                            'Next': 'Save fail run'
                        },
                    ],
                    'Next': next_state
                }
                failure_prone = True

            elif action_type == 'send_app_message':
                definition['States'][name] = {
                    'Type': 'Task',
                    'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                    'InputPath': '$',
                    'Parameters': {
                        'state_name.$': '$$.State.Name',
                        'task_type': action_type,
                        'journey_id': journey_id,
                        'journey_run_id.$': '$.journey_run_id'
                    },
                    'OutputPath': '$',
                    'Catch': [
                        {
                            'ErrorEquals': ['States.ALL'],
                            'Next': 'Save fail run'
                        },
                    ],
                    'Next': next_state
                }
                failure_prone = True

            elif action_type == 'send_email_message':
                definition['States'][name] = {
                    'Type': 'Task',
                    'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                    'InputPath': '$',
                    'Parameters': {
                        'state_name.$': '$$.State.Name',
                        'task_type': action_type,
                        'journey_id': journey_id,
                        'journey_run_id.$': '$.journey_run_id'
                    },
                    'OutputPath': '$',
                    'Catch': [
                        {
                            'ErrorEquals': ['States.ALL'],
                            'Next': 'Save fail run'
                        },
                    ],
                    'Next': next_state
                }
                failure_prone = True

            elif action_type == 'send_reward':
                definition['States'][name] = {
                    'Type': 'Task',
                    'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                    'InputPath': '$',
                    'Parameters': {
                        'state_name.$': '$$.State.Name',
                        'task_type': action_type,
                        'journey_id': journey_id,
                        'journey_run_id.$': '$.journey_run_id'
                    },
                    'OutputPath': '$',
                    'Catch': [
                        {
                            'ErrorEquals': ['States.ALL'],
                            'Next': 'Save fail run'
                        },
                    ],
                    'Next': next_state
                }
                failure_prone = True

            elif action_type == 'tag_contact':
                definition['States'][name] = {
                    'Type': 'Task',
                    'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                    'InputPath': '$',
                    'Parameters': {
                        'state_name.$': '$$.State.Name',
                        'task_type': action_type,
                        'journey_id': journey_id,
                        'journey_run_id.$': '$.journey_run_id'
                    },
                    'OutputPath': '$',
                    'Catch': [
                        {
                            'ErrorEquals': ['States.ALL'],
                            'Next': 'Save fail run'
                        },
                    ],
                    'Next': next_state
                }
                failure_prone = True

            elif action_type in ['match_all', 'match_any']:
                state_name = name
                choice_state_name = f'Contact matched?'

                # Get data for the choice state
                definition['States'][state_name] = {
                    'Type': 'Task',
                    'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                    'InputPath': '$',
                    'Parameters': {
                        'state_name.$': '$$.State.Name',
                        'task_type': action_type,
                        'journey_id': journey_id,
                        'journey_run_id.$': '$.journey_run_id'
                    },
                    'OutputPath': '$',
                    'Catch': [
                        {
                            'ErrorEquals': ['States.ALL'],
                            'Next': 'Save fail run'
                        },
                    ],
                    'Next': choice_state_name
                }
                failure_prone = True

                # Choice state
                definition['States'][choice_state_name] = {
                    'Type': 'Choice',
                    'Choices': [
                        {
                            'Variable': '$.match',
                            'BooleanEquals': True,
                            'Next': next_state
                        }
                    ],
                    'Default': 'Save success run'
                }

            elif action_type == 'wait':
                definition['States'][name] = {
                    'Type': 'Wait',
                    'Seconds': versify_definition['config']['seconds'],
                    'Next': next_state
                }

            else:
                print(f'Invalid action type: {action_type}')
                raise Exception('Invalid state type')

        # Insert success states
        definition['States']['Save success run'] = {
            'Type': 'Task',
            'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
            'InputPath': '$',
            'Parameters': {
                'state_name.$': '$$.State.Name',
                'task_type': 'update_run',
                'journey_id': journey_id,
                'journey_run_id.$': '$.journey_run_id',
                'status': 'completed'
            },
            'OutputPath': '$',
            'Next': 'Success'
        }
        definition['States']['Success'] = {
            'Type': 'Succeed'
        }

        # Insert failure states
        if failure_prone:
            definition['States']['Save fail run'] = {
                'Type': 'Task',
                'Resource': Config.STEP_FUNCTION_LAMBDA_ARN,
                'InputPath': '$',
                'Parameters': {
                    'state_name.$': '$$.State.Name',
                    'task_type': 'update_run',
                    'journey_id': journey_id,
                    'journey_run_id.$': '$.journey_run_id',
                    'status': 'failed'
                },
                'OutputPath': '$',
                'Next': 'Fail'
            }
            definition['States']['Fail'] = {
                'Type': 'Fail'
            }

        return definition

    def sync_resoures(self, journey: dict, create: bool = True) -> dict:
        """Create journey resources

        Args:
            journey (dict): The journey to create resources for
            create (bool, optional): Whether to create resources. Defaults to True.

        Returns:
            dict: The journey with resources
        """

        # Create step function with states from journey
        sfn_arn = Config.STEP_FUNCTION_ARN_BASE + journey['id']
        if create:
            create_state_machine(
                name=journey['id'],
                definition=self.journey_to_definition(journey),
                role_arn=Config.STEP_FUNCTION_ROLE_ARN,
                log_arn=Config.STEP_FUNCTION_LOG_ARN
            )
        else:
            update_state_machine(
                arn=sfn_arn,
                definition=self.journey_to_definition(journey),
                role_arn=Config.STEP_FUNCTION_ROLE_ARN
            )

        # Create trigger (event bus rule or schedule)
        enabled = journey['active']
        trigger = journey['trigger']
        if trigger['type'] == 'event':
            event_pattern = self.journey_to_event_pattern(journey)
            create_rule(
                name=journey['id'],
                event_bus='versify',
                event_pattern=event_pattern,
                enabled=enabled
            )
            create_target(
                rule=journey['id'],
                event_bus='versify',
                target_arn=sfn_arn,
                role_arn=Config.STEP_FUNCTION_ROLE_ARN
            )
        elif trigger['type'] == 'schedule':
            expression, start, end = self.journey_to_schedule(journey)
            if create:
                create_schedule(
                    name=journey['id'],
                    expression=expression,
                    target=sfn_arn,
                    role=Config.STEP_FUNCTION_ROLE_ARN,
                    enabled=enabled,
                    start=start,
                    end=end
                )
            else:
                update_schedule(
                    name=journey['id'],
                    expression=expression,
                    target=sfn_arn,
                    role=Config.STEP_FUNCTION_ROLE_ARN,
                    enabled=enabled,
                    start=start,
                    end=end
                )
        else:
            raise Exception('Invalid trigger type')

        return journey

    def create(self, body: dict) -> dict:
        """Create a new journey. If the journey already exists, update the journey.

        Args:
            body (dict): The journey to create.

        Returns:
            dict: The journey.
        """
        print('Creating journey')

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Validate against schema
        data = self.Model(**body)

        # Create resources
        self.sync_resoures(data.to_json(), create=True)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        journey = data.to_json()

        return journey

    def count(self, filter: dict) -> int:
        """Count journeys.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of journeys.
        """

        # Get journeys from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List journeys.

        Args:
            query (dict): The query to use.

        Returns:
            list: The journeys.
        """
        print('Listing journeys')

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def get(self, journey_id: str) -> dict:
        """Get an journey by id.

        Args:
            journey_id (str): The id of the journey to retrieve.

        Returns:
            dict: The journey.
        """
        print('Retrieving journey')

        # Find document matching filter
        journey = self.collection.find_one(filter={'_id': journey_id})
        if not journey:
            raise NotFoundError

        # Convert to JSON
        journey = self.Model(**journey).to_json()

        return journey

    def update(self, journey_id: str, body: dict) -> dict:
        """Update a journey.

        Args:
            journey_id (str): The id of the journey to update.
            body (dict): The fields to update.

        Returns:
            dict: The updated journey.

        Raises:
            NotFoundError: If the journey does not exist.
        """
        print('Updating journey')

        # Find document matching filter
        journey = self.collection.find_one(filter={'_id': journey_id})
        if not journey:
            raise NotFoundError

        # Update fields
        journey = deep_update(journey, body)
        journey['updated'] = int(time.time())

        # Validate against schema
        validated_journey = self.Model(**journey)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': journey_id},
            update={'$set': validated_journey.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        # Create resources
        self.sync_resoures(data, create=False)

        return data

    def duplicate(self, journey_id: str) -> dict:
        """Duplicate a journey

        Args:
            journey_id (str): ID of the journey to duplicate

        Returns:
            dict: JourneyRun
        """
        print('Duplicating journey...')
        journey = self.get(journey_id)
        new_journey_body = dict(journey)
        new_journey_body['active'] = False
        new_journey_body['name'] = 'Duplicate of ' + new_journey_body['name']
        new_journey = self.create(new_journey_body)
        return new_journey

    def delete(self, journey_id: str) -> bool:
        """Delete a journey.

        Args:
            journey_id (str): The id of the journey to delete.

        Returns:
            bool: True if the journey was deleted, False otherwise.
        """
        print('Deleting journey')

        # Delete item from DB
        result = self.collection.delete_one(filter={'_id': journey_id})

        # Delete resources
        delete_state_machine(Config.STEP_FUNCTION_ARN_BASE + journey_id)
        try:
            delete_rule(name=journey_id, event_bus='versify')
            remove_targets(rule=journey_id, event_bus='versify')
        except Exception as e:
            print(e)
        try:
            delete_schedule(name=journey_id)
        except Exception as e:
            print(e)

        return result.deleted_count == 1
