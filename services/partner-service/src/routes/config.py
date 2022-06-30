import os
import secrets

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..utils.auth0 import auth0
from ..utils.stripe import BasicPackage, GrowthPackage, stripe

app = APIGatewayRestResolver(strip_prefixes=["/partners"])
logger = Logger()
tracer = Tracer()


def get_billing_usage(upcoming_invoice):

    # Get the customers usage
    plan = ''
    usage = {'collections': 0,  'mints': 0}
    limits = {'collections': 0,  'mints': 0}
    for line in upcoming_invoice['lines']['data']:

        # If its collections, add to collections qty
        if line['price']['nickname'] == 'collections':
            usage['collections'] += line['quantity']
            limits['collections'] = line['price']['tiers'][0]['up_to']

        # If its mints, add to mints qty
        elif line['price']['nickname'] == 'mints':
            usage['mints'] += line['quantity']
            limits['mints'] = line['price']['tiers'][0]['up_to']

        # If its neither, it must be the package
        elif line['price']['nickname'] in ['basic', 'growth', 'enterprise']:
            plan = line['price']['nickname']

    return {
        'plan': plan,
        'usage': usage,
        'limits': limits,
    }


@app.get("/all/config")
@tracer.capture_method
def get_config():
    authorizer = app.current_event.request_context.authorizer or {}

    # Auth0 User
    if authorizer.get('user'):
        user_id = authorizer.get('user')
        user = auth0.users.get(user_id)
        user_organizations = auth0.users.list_organizations(user_id)
        user['organizations'] = user_organizations['organizations']
    else:
        user = None

    # Auth0 Organization
    if authorizer.get('organization'):
        org_id = authorizer.get('organization')
        org = auth0.organizations.get_organization(org_id)
    else:
        org = None

    # Stripe Customer
    customer_id = org['metadata'].get('stripe_customer') if org else None
    if org and customer_id:
        customer = stripe.Customer.retrieve(
            customer_id,
            expand=['invoice_settings.default_payment_method']
        )
        org['customer'] = customer

    # Stripe Subscription
    sub_id = org['metadata'].get('stripe_subscription') if org else None
    if org and sub_id:
        subscription = stripe.Subscription.retrieve(
            sub_id
        )
        org['subscription'] = subscription

    # Stripe Upcoming Invoice
    if org and customer_id and sub_id:
        upcoming_invoice = stripe.Invoice.upcoming(
            customer=customer_id,
            subscription=sub_id,
            expand=['lines.data.price.tiers']
        )
        org['upcoming_invoice'] = upcoming_invoice
        org['package'] = get_billing_usage(upcoming_invoice)

    return {
        'user': user,
        'organization': org
    }


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
