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


@app.post("/admin/collections")
@tracer.capture_method
def create_collection():
    versify = sync(app)
    payload = app.current_event.json_body
    collection = versify.collections.create(payload)
    return response('create', collection)


@app.get("/admin/collections")
@tracer.capture_method
def list_collections():
    versify = sync(app)
    collections = versify.collections.list()
    return response('list', collections, 'collection', '/collections', False)


@app.get("/admin/collections/<id>")
@tracer.capture_method
def get_collection(id):
    versify = sync(app)
    collection = versify.collections.get(id)
    return response('get', collection)


@app.put("/admin/collections/<id>")
@tracer.capture_method
def update_collection(id):
    versify = sync(app)
    payload = app.current_event.json_body
    collection = versify.collections.update(id, payload)
    return response('update', collection)


@app.post("/admin/products")
@tracer.capture_method
def create_product():
    versify = sync(app)
    payload = app.current_event.json_body
    product = versify.products.create(payload)
    return response('create', product)


@app.get("/admin/products")
@tracer.capture_method
def list_products():
    versify = sync(app)
    products = versify.products.list()
    return response('list', products, 'product', '/products', False)


@app.get("/admin/products/<id>")
@tracer.capture_method
def get_product(id):
    versify = sync(app)
    product = versify.products.get(id)
    return response('get', product)


@app.get("/backend/products/<id>")
@tracer.capture_method
def get_product(id):
    versify = sync(app)
    product = versify.products.get(id)
    return response('get', product)


@app.put("/admin/products/<id>")
@tracer.capture_method
def update_product(id):
    versify = sync(app)
    payload = app.current_event.json_body
    product = versify.products.update(id, payload)
    return response('update', product)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
