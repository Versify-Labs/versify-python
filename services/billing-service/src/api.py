import json
import os

import stripe
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities import parameters
from lambda_decorators import cors_headers

from .eb import publish_event

AIRDROP_LIMIT_BASE = 25
AIRDROP_LIMIT_GROWTH = 1000
AIRDROP_LIMIT_ENTERPRISE = 10000
SECRET = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET)
STRIPE_PUBLIC_KEY = SECRET.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = SECRET.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = SECRET.get('STRIPE_WEBHOOK_SECRET')

stripe.api_key = STRIPE_SECRET_KEY

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@tracer.capture_method
def sync(app):
    authorizer = app.current_event.request_context.authorizer
    customer = authorizer.get('stripe_customer')
    if not customer:
        raise BadRequestError('Customer is required for all billing endpoints')
    return True


def get_active_subscription(customer_id):
    subscriptions = stripe.Subscription.list(
        customer=customer_id,
        status='active',
        expand=['data.default_payment_method']
    )
    logger.info(subscriptions)
    if not subscriptions or len(subscriptions) < 1:
        return
    subscription = subscriptions.data[0]
    return subscription


def get_airdrop_limit(plan_name):
    plan_map = {
        'basic': AIRDROP_LIMIT_BASE,
        'growth': AIRDROP_LIMIT_GROWTH,
        'enterprise': AIRDROP_LIMIT_ENTERPRISE,
    }
    return plan_map[plan_name] if plan_name in plan_map else 0


@app.get("/billing/v1/config")
@tracer.capture_method
def get_config():
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    customer_id = authorizer.get('stripe_customer')
    customer = stripe.Customer.retrieve(
        customer_id,
        expand=['invoice_settings.default_payment_method']
    )
    prices = stripe.Price.list(
        active=True,
        currency='usd',
        expand=['data.product'],
        lookup_keys=['basic', 'growth', 'enterprise'],
        type='recurring'
    )
    return {
        'customer': customer,
        'public_key': STRIPE_PUBLIC_KEY,
        'plans': prices.data,
        'subscription': get_active_subscription(customer_id),
    }


@app.get("/billing/v1/customer")
@tracer.capture_method
def get_customer():
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    customer = authorizer.get('stripe_customer')
    customer = stripe.Customer.retrieve(
        customer,
        expand=['invoice_settings.default_payment_method']
    )
    return customer


@app.get("/billing/v1/invoices")
@tracer.capture_method
def list_invoices():
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    customer = authorizer.get('stripe_customer')
    invoices = stripe.Invoice.list(
        customer=customer
    )
    return invoices


@app.post("/billing/v1/payment_methods")
@tracer.capture_method
def create_payment_method():
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    payload = app.current_event.json_body

    # Parse request for needed fields
    customer = authorizer.get('stripe_customer')
    payment_method_id = payload['payment_method']

    # Attach the payment method to the customer
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer
    )

    # Set the default payment method on the customer
    updated_customer = stripe.Customer.modify(
        customer,
        invoice_settings={'default_payment_method': payment_method_id}
    )

    return updated_customer


@app.get("/billing/v1/subscriptions")
@tracer.capture_method
def list_subscriptions():
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    customer = authorizer.get('stripe_customer')
    subscriptions = stripe.Subscription.list(
        customer=customer
    )
    return subscriptions


@app.post("/billing/v1/subscriptions")
@tracer.capture_method
def create_subscription():
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    payload = app.current_event.json_body

    # Parse request for needed fields
    customer = authorizer.get('stripe_customer')
    price = payload.get('price')
    logger.info({
        'customer': customer,
        'price': price
    })

    # Create the subscription
    subscription = stripe.Subscription.create(
        customer=customer,
        items=[{'price': price}]
    )
    return subscription


@app.put("/billing/v1/subscriptions/<subscription_id>")
@tracer.capture_method
def update_subscription(subscription_id):
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    payload = app.current_event.json_body

    # Parse request for needed fields
    customer = authorizer.get('stripe_customer')
    price = payload.get('price')
    logger.info({
        'customer': customer,
        'price': price
    })

    # Get the current subscription
    subscription = stripe.Subscription.retrieve(subscription_id)

    # Update the subscription
    subscription = stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=False,
        items=[{
            'id': subscription['items']['data'][0].id,
            'price': price
        }]
    )
    return subscription


@app.get("/billing/v1/subscriptions/<subscription_id>/usage")
@tracer.capture_method
def get_subscription_usage(subscription_id):
    sync(app)
    authorizer = app.current_event.request_context.authorizer
    customer = authorizer.get('stripe_customer')

    # Get the upcoming invoice and associated usage
    invoice = stripe.Invoice.upcoming(
        customer=customer,
        subscription=subscription_id
    )
    airdrops_sent = 0
    plan_name = ''
    for item in invoice['lines']['data']:
        plan_name = item['price']['lookup_key']
        airdrops_sent += item['quantity']
    return {
        'airdrops_limit': get_airdrop_limit(plan_name),
        'airdrops_sent': airdrops_sent,
        'amount_due': invoice['amount_due'],
        'invoice': invoice,
        'plan_name': plan_name,
        'subscription': subscription_id,
    }


@app.post("/billing/v1/webhook")
@tracer.capture_method
def webhook():
    signature = app.current_event.get_header_value("Stripe-Signature")
    payload = app.current_event.raw_event['body']
    wh_secret = STRIPE_WEBHOOK_SECRET
    detail_type = ''
    detail = {}
    source = 'stripe'
    try:
        event = stripe.Webhook.construct_event(payload, signature, wh_secret)
        detail_type = event['type']
        detail = event['data']['object']
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e
    return publish_event(detail_type, detail, source)


@cors_headers()
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
