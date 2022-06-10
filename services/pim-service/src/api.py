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
    organization = app.current_event.get_header_value('X-Organization')
    versify = Versify(organization)
    return versify


@app.post("/pim/v1/collections")
@tracer.capture_method
def create_collection():
    versify = sync(app)
    payload = app.current_event.json_body
    collection = versify.collections.create(payload)
    return response('create', collection)


@app.get("/pim/v1/collections")
@tracer.capture_method
def list_collections():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters
    collections = versify.collections.list(query_params)
    return response('list', collections, 'collection', '/collections', False)


@app.get("/pim/v1/collections/<collection_id>")
@tracer.capture_method
def get_collection(collection_id):
    versify = sync(app)
    collection = versify.collections.get(collection_id)
    return response('get', collection)


@app.put("/pim/v1/collections/<collection_id>")
@tracer.capture_method
def update_collection(collection_id):
    versify = sync(app)
    payload = app.current_event.json_body
    collection = versify.collections.update(collection_id, payload)
    return response('update', collection)


@app.put("/pim/v1/collections/<collection_id>/actions/archive")
@tracer.capture_method
def archive_collection(collection_id):
    versify = sync(app)
    collection = versify.collections.archive(collection_id)
    return response('update', collection)


@app.put("/pim/v1/collections/<collection_id>/actions/unarchive")
@tracer.capture_method
def unarchive_collection(collection_id):
    versify = sync(app)
    collection = versify.collections.unarchive(collection_id)
    return response('update', collection)


@app.post("/pim/v1/products")
@tracer.capture_method
def create_product():
    versify = sync(app)
    payload = app.current_event.json_body
    product = versify.products.create(payload)
    return response('create', product)


@app.get("/pim/v1/products")
@tracer.capture_method
def list_products():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters
    products = versify.products.list(query_params)
    return response('list', products, 'product', '/products', False)


@app.get("/pim/v1/products/<product_id>")
@tracer.capture_method
def get_product(product_id):
    versify = sync(app)
    product = versify.products.get(product_id)
    return response('get', product)


@app.get("/pim/v1/backend/products/<product_id>")
@tracer.capture_method
def get_product(product_id):
    versify = sync(app)
    product = versify.products.get(product_id)
    return response('get', product)


@app.put("/pim/v1/products/<product_id>")
@tracer.capture_method
def update_product(product_id):
    versify = sync(app)
    payload = app.current_event.json_body
    product = versify.products.update(product_id, payload)
    return response('update', product)


@app.put("/pim/v1/products/<product_id>/actions/archive")
@tracer.capture_method
def archive_product(product_id):
    versify = sync(app)
    product = versify.products.archive(product_id)
    return response('update', product)


@app.put("/pim/v1/products/<product_id>/actions/unarchive")
@tracer.capture_method
def unarchive_product(product_id):
    versify = sync(app)
    product = versify.products.unarchive(product_id)
    return response('update', product)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
