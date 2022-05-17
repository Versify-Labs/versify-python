from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers
from versify.utilities.model import response

from .service import Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@tracer.capture_method
def sync(app):
    authorizer = app.current_event.request_context.authorizer
    email = authorizer.get('email')
    organization = app.current_event.get_header_value('Organization')
    versify = Versify(email, organization)
    return versify


@app.post("/admin/airdrops")
@tracer.capture_method
def create_airdrop():
    versify = sync(app)
    payload = app.current_event.json_body
    airdrop = versify.airdrops.create(payload)
    return response('create', airdrop)


@app.get("/admin/orders")
@tracer.capture_method
def list_admin_orders():
    versify = sync(app)
    query = app.current_event.query_string_parameters or {}
    orders = versify.orders.list_by_organization(query)
    return response('list', orders, 'order', '/orders', False)


@app.get("/admin/orders/<id>")
@tracer.capture_method
def get_admin_order(id):
    versify = sync(app)
    order = versify.orders.get(id)
    return response('get', order)


@app.get("/admin/orders/<id>/fulfillments")
@tracer.capture_method
def list_fulfillments(id):
    versify = sync(app)
    fulfillments = versify.fulfillments.list_by_order(id)
    return response('list', fulfillments, 'fulfillments', '/fulfillments', False)


@app.get("/wallet/orders")
@tracer.capture_method
def list_wallet_orders():
    versify = sync(app)
    orders = versify.orders.list_by_email()
    return response('list', orders, 'order', '/orders', False)


# @app.post("/wallet/orders/<id>/fulfillments")
# @tracer.capture_method
# def create_fulfillment(id):
#     authorizer = app.current_event.request_context.authorizer
#     publicAddress = authorizer.get('publicAddress')
#     versify = sync(app)
#     payload = app.current_event.json_body
#     payload['blockchain_address'] = publicAddress
#     fulfillment = versify.fulfillments.create(id, payload)
#     return response('create', fulfillment)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
