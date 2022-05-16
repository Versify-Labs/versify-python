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
    organization = app.current_event.get_header_value('Organization')
    versify = Versify(organization)
    return versify


@app.post("/admin/customers")
@tracer.capture_method
def create_customer():
    versify = sync(app)
    payload = app.current_event.json_body
    customer = versify.customers.create(payload)
    return response('create', customer)


@app.get("/admin/customers")
@tracer.capture_method
def list_customers():
    versify = sync(app)
    customers = versify.customers.list()
    return response('list', customers, 'customer', '/customers', False)


@app.get("/admin/customers/<id>")
@tracer.capture_method
def get_customer(id):
    versify = sync(app)
    customer = versify.customers.get(id)
    return response('get', customer)


@app.get("/backend/customers/<id>")
@tracer.capture_method
def get_customer(id):
    versify = sync(app)
    customer = versify.customers.get(id)
    return response('get', customer)


@app.put("/admin/customers/<id>")
@tracer.capture_method
def update_customer(id):
    versify = sync(app)
    payload = app.current_event.json_body
    customer = versify.customers.update(id, payload)
    return response('update', customer)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
