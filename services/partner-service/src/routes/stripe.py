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


def get_organization_customer(org):
    org = auth0.organizations.get_organization(org)
    return org['metadata'].get('stripe_customer')


@app.get("/stripe/customer")
@tracer.capture_method
def get_customer():
    authorizer = app.current_event.request_context.authorizer
    organization = authorizer.get('organization')
    customer_id = get_organization_customer(organization)
    customer = stripe.Customer.retrieve(
        customer_id,
        expand=['invoice_settings.default_payment_method']
    )
    return customer


@app.get("/stripe/invoices")
@tracer.capture_method
def list_invoices():
    authorizer = app.current_event.request_context.authorizer
    organization = authorizer.get('organization')
    customer_id = get_organization_customer(organization)
    invoices = stripe.Invoice.list(
        customer=customer_id
    )
    logger.info(invoices)
    for invoice in invoices['data']:
        logger.info(invoice)
        for line in invoice['lines']['data']:
            line['product'] = stripe.Product.retrieve(
                line['price']['product']
            )
            logger.info(line)
    return invoices


@app.get("/stripe/subscriptions")
@tracer.capture_method
def list_subscriptions():
    organization = app.current_event.get_header_value('X-Organization')
    customer_id = get_organization_customer(organization)
    subscriptions = stripe.Subscription.list(
        customer=customer_id
    )
    return subscriptions


@app.post("/stripe/payment_methods")
@tracer.capture_method
def create_payment_method():
    authorizer = app.current_event.request_context.authorizer
    payload = app.current_event.json_body

    # Parse request for needed fields
    payment_method_id = payload['payment_method']
    organization = authorizer.get('organization')
    customer_id = get_organization_customer(organization)

    # Attach the payment method to the customer
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # Set the default payment method on the customer
    updated_customer = stripe.Customer.modify(
        customer_id,
        invoice_settings={'default_payment_method': payment_method_id}
    )

    return updated_customer


@app.put("/stripe/subscriptions/<id>")
@tracer.capture_method
def update_subscription(id):
    authorizer = app.current_event.request_context.authorizer
    payload = app.current_event.json_body

    # Parse request for needed fields
    organization = authorizer.get('organization')
    customer_id = get_organization_customer(organization)
    plan = payload.get('plan')
    logger.info({
        'customer': customer_id,
        'plan': plan
    })

    # Get the current subscription
    subscription = stripe.Subscription.retrieve(id)

    # Update the subscription
    new_package = BasicPackage if plan == 'basic' else GrowthPackage
    new_items = []
    for item in subscription['items']['data']:

        # Update the package item to the new plans package price
        if item['price']['nickname'] in ['basic', 'growth']:
            new_items.append(
                {
                    'id': item.id,
                    'price': new_package.PACKAGE_PRICE
                }
            )

        # Update the collections item to the new plans contract price
        if item['price']['nickname'] == 'collections':
            new_items.append(
                {
                    'id': item.id,
                    'price': new_package.COLLECTION_PRICE
                }
            )

        # Update the mints item to the new plans mint price
        if item['price']['nickname'] == 'mints':
            new_items.append(
                {
                    'id': item.id,
                    'price': new_package.MINT_PRICE
                }
            )

    subscription = stripe.Subscription.modify(
        id,
        cancel_at_period_end=False,
        items=new_items
    )
    return subscription


@app.post("/stripe/usage_records")
@tracer.capture_method
def create_usage_record():
    payload = app.current_event.json_body

    # Parse request for needed fields
    subscription_item = payload['subscription_item']
    timestamp = payload['timestamp']
    quantity = payload.get('quantity', 1)

    # Create the usage record for the subscription item
    record = stripe.SubscriptionItem.create_usage_record(
        subscription_item,
        quantity=quantity,
        timestamp=timestamp,
    )
    logger.info(record)

    return record


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
