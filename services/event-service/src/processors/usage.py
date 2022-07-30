from aws_lambda_powertools import Logger

from ..utils.api import call_api
from ..utils.stripe import stripe

logger = Logger()


class UsageProcessor:

    def __init__(self, object) -> None:
        self.object = object

    def validate(self):
        return True

    def get_account(self):
        account_id = self.object['account']
        account = call_api(
            method='GET',
            path=f'/internal/accounts/{account_id}',
            account=account_id
        )
        return account

    def get_subscription_item(self, account):
        subscriptions = account['settings']['billing']['subscriptions']
        for _, subscription in subscriptions:
            for item in subscription['items']['data']:
                return item
        return None

    def create_usage_record(self, subscription_item):
        record = stripe.SubscriptionItem.create_usage_record(
            subscription_item['id'],
            timestamp=self.object['created'],
            quantity=1
        )
        logger.info(record)
        return record

    def start(self):
        self.validate()
        account = self.get_account()
        subscription_item = self.get_subscription_item(account)
        record = self.create_usage_record(subscription_item)
        return record
