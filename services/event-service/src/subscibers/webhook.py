from aws_lambda_powertools import Logger, Tracer

from ..utils.api import call_api, call_external_api
from ._base import BaseSubscriber

logger = Logger()


class WebhookSubscriber(BaseSubscriber):

    def start(self, event):

        # Parse event for params
        organization = event.detail.get('organization')

        # Save Event to DB
        event_response = call_api(
            method='POST',
            path='/internal/events',
            body={
                'data': {
                    'object': event.detail
                },
                'type': event.detail_type
            }
        )
        logger.info(event_response)

        # Webhooks are for organization events only
        if not organization:
            return

        # Get all matching webhooks this event needs to be sent to
        webhooks_response = call_api(
            method='GET',
            path='/internal/webhooks',
            params={
                'active': 'true',
                'enabled_events': event.detail_type,
                'organization': organization
            }
        )
        logger.info(webhooks_response)

        # Send webhook events
        for webhook in webhooks_response.get('data', []):
            logger.info('Calling webhook:')
            logger.info(webhook)

            response = call_external_api(
                method='POST',
                url=webhook['url'],
                organization=organization,
                body=event_response
            )
            logger.info(response)

        # TODO: Update Event to DB with the response
        return True
