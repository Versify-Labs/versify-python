from aws_lambda_powertools import Logger

from ..utils.api import call_api
from ..utils.stripe import stripe

logger = Logger()


class BillingProcessor:

    def __init__(self, event) -> None:
        self.event = event

    def validate(self):
        return True

    def update_account(self, customer_id, object):

        # Get customer from stripe (to get the versify account)
        customer = stripe.Customer.retrieve(
            customer_id,
            expand=['default_source', 'invoice_settings.default_payment_method']
        )
        account_id = customer['metadata']['account']

        # Get Versify account
        account = call_api(
            method='GET',
            path=f'/internal/accounts/{account_id}',
            account=account_id
        )
        logger.info(account)

        # Update Versify account
        settings = account['settings']
        billing = settings['billing']

        if object['object'] == 'customer':

            # Update customer data
            billing['customer'] = customer

        elif object['object'] == 'subscription':

            # Update customer data
            billing['customer'] = customer

            # Update subscription data
            sub_id = object['id']
            subs = billing.get('subscriptions') or {}
            subs[sub_id] = object
            billing['subscriptions'] = subs

            # Update upcoming invoice for subscription (to keep usage up to date)
            upcoming_invoice = stripe.Invoice.upcoming(
                customer=customer_id,
                subscription=sub_id,
                expand=['lines.data.price.tiers']
            )
            billing['upcoming_invoice'] = upcoming_invoice

        settings['billing'] = billing
        body = {'settings': settings}
        logger.info(body)

        account = call_api(
            method='PUT',
            path=f'/internal/accounts/{account_id}',
            body=body,
            account=account_id
        )
        logger.info(account)
        return True

    def on_customer_created(self):
        """Handle new customer"""
        object = self.event['data']['object']
        customer_id = object['id']
        return self.update_account(customer_id, object)

    def on_customer_updated(self):
        """Handle updated customer"""
        object = self.event['data']['object']
        customer_id = object['id']
        return self.update_account(customer_id, object)

    def on_subscription_created(self):
        """Handle new customer subscription"""
        object = self.event['data']['object']
        customer_id = object['customer']
        return self.update_account(customer_id, object)

    def on_subscription_updated(self):
        """Handle updated customer subscription"""
        object = self.event['data']['object']
        customer_id = object['customer']
        return self.update_account(customer_id, object)

    def start(self):

        # TODO: Validate event came from stripe
        self.validate()

        # Get the type of webhook event sent
        event_type = self.event['type']
        print('event ' + event_type)

        # Handle event accordingly
        if event_type == 'customer.created':
            return self.on_customer_created()
        elif event_type == 'customer.updated':
            return self.on_customer_updated()
        elif event_type == 'customer.subscription.created':
            return self.on_subscription_created()
        elif event_type == 'customer.subscription.updated':
            return self.on_subscription_updated()
        else:
            logger.error('Unknown event type')

        return True
