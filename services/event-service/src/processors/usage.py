import os

from aws_lambda_powertools import Logger

from ..utils.api import call_api

logger = Logger()

ENVIRONMENT = os.environ['ENVIRONMENT']
if ENVIRONMENT == 'prod':
    DASHBOARD_URL = 'https://dashboard.versifylabs.com'
else:
    DASHBOARD_URL = 'https://dashboard-dev.versifylabs.com'
CLAIM_URL = DASHBOARD_URL + '/wallet/claims'


class UsageProcessor:

    def __init__(self, object) -> None:
        self.object = object

    def validate(self):
        return True

    def get_organization(self):
        org_id = self.object['organization']
        organization = call_api(
            method='GET',
            path=f'/partners/auth0/organizations/{org_id}/validate',
            organization=self.object['organization']
        )
        logger.info(organization)
        return organization

    def get_subscription_item(self, customer_id):
        subscriptions = call_api(
            method='GET',
            path='/partners/stripe/subscriptions',
            organization=self.object['organization'],
            params={'customer': customer_id}
        )
        logger.info(subscriptions)

        for subscription in subscriptions['data']:
            logger.info('Checking the following subscription')
            logger.info(subscription)

            for item in subscription['items']['data']:
                logger.info('Checking the following subscription item')
                logger.info(item)

                if self.object['object'] in item['plan']['nickname']:
                    return item

        return None

    def create_usage_record(self, subscription_item):
        product = call_api(
            method='POST',
            path='/partners/stripe/usage_records',
            organization=self.object['organization'],
            body={
                'subscription_item': subscription_item['id'],
                'timestamp': self.object['created'],
                'quantity': 1
            }
        )
        logger.info(product)
        return product

    def start(self):
        self.validate()
        organization = self.get_organization()
        customer_id = organization['metadata'].get('stripe_customer')
        subscription_item = self.get_subscription_item(customer_id)
        record = self.create_usage_record(subscription_item)
        return record
