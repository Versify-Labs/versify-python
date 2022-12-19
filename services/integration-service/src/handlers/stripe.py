from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from versify import Versify

from ..utils.stripe import stripe

tracer = Tracer()
logger = Logger()
versify = Versify()


def update_account(customer_id, object):

    # Get customer from stripe (to get the versify account)
    customer = stripe.Customer.retrieve(
        customer_id,
        expand=['default_source', 'invoice_settings.default_payment_method']
    )
    account_id = customer['metadata']['account']
    logger.info(customer)

    # Refresh account billing settings
    versify.account_service.refresh_billing_settings(account_id)

    return True


def on_customer_created(event):
    """Handle new customer"""
    object = event['data']['object']
    customer_id = object['id']
    return update_account(customer_id, object)


def on_customer_updated(event):
    """Handle updated customer"""
    object = event['data']['object']
    customer_id = object['id']
    return update_account(customer_id, object)


def on_subscription_created(event):
    """Handle new customer subscription"""
    object = event['data']['object']
    customer_id = object['customer']
    return update_account(customer_id, object)


def on_subscription_updated(event):
    """Handle updated customer subscription"""
    object = event['data']['object']
    customer_id = object['customer']
    return update_account(customer_id, object)


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    stripe_event = event.detail

    # Get the type of webhook event sent
    event_type = stripe_event['type']

    # Handle event accordingly
    if event_type == 'customer.created':
        return on_customer_created(stripe_event)
    elif event_type == 'customer.updated':
        return on_customer_updated(stripe_event)
    elif event_type == 'customer.subscription.created':
        return on_subscription_created(stripe_event)
    elif event_type == 'customer.subscription.updated':
        return on_subscription_updated(stripe_event)
    else:
        logger.error('Unknown event type')

    return True
