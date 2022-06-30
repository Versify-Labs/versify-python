from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Product

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
resource = Product()


@app.get('/internal/products/<products_id>')
@tracer.capture_method
def internal_get(products_id):
    return resource.get(app, products_id)


@app.put('/internal/products/<products_id>')
@tracer.capture_method
def internal_update(products_id):
    return resource.update(app, products_id)


@app.get('/v1/products')
@tracer.capture_method
def list():
    return resource.list(app)


@app.post('/v1/products')
@tracer.capture_method
def create():
    return resource.create(app)


@app.get('/v1/products/<products_id>')
@tracer.capture_method
def get(products_id):
    return resource.get(app, products_id)


@app.put('/v1/products/<products_id>')
@tracer.capture_method
def update(products_id):
    return resource.update(app, products_id)


@app.delete('/v1/products/<products_id>')
@tracer.capture_method
def delete(products_id):
    return resource.delete(app, products_id)


@app.put('/v1/products/<id>/activate')
@tracer.capture_method
def activate(id):
    return resource.activate(app, id)


@app.put('/v1/products/<id>/archive')
@tracer.capture_method
def archive(id):
    return resource.archive(app, id)


@app.put('/v1/products/<id>/tag')
@tracer.capture_method
def tag(id):
    return resource.tag(app, id)


@app.get('/v1/products/aggregate/search')
@tracer.capture_method
def search():
    return resource.search(app)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
