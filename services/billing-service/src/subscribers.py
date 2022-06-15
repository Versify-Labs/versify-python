import json
import os
import time
import uuid

import stripe
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

SECRET = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET)
STRIPE_SECRET_KEY = SECRET.get('STRIPE_SECRET_KEY')
stripe.api_key = STRIPE_SECRET_KEY

tracer = Tracer()
logger = Logger()


def get_active_subscription_item(customer_id):
    subscriptions = stripe.Subscription.list(
        customer=customer_id,
        status='active',
        expand=['data.default_payment_method']
    )
    logger.info(subscriptions)
    if not subscriptions or len(subscriptions.data) < 1:
        return
    subscription = subscriptions.data[0]
    return subscription['items'].data[0]


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_airdrop_created(event, context):
    """Create a usage record in Stripe"""
    airdrop = event.detail

    # Get organizations subscription
    customer_id = airdrop['organization_details']['metadata']['stripe_customer']
    subscription_item = get_active_subscription_item(customer_id)
    if not subscription_item:
        logger.error('No active subscription found')
        return
    subscription_item_id = subscription_item['id']

    # The usage number from the new airdrop
    usage_quantity = 1

    # The idempotency key allows you to retry this usage record call if it fails.
    idempotency_key = str(uuid.uuid4())

    # Create usage record for subscription
    stripe.SubscriptionItem.create_usage_record(
        subscription_item_id,
        quantity=usage_quantity,
        timestamp=int(time.time()),
        action='set',
        idempotency_key=idempotency_key
    )

    return True
