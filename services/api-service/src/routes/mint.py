from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Mint

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
resource = Mint()


@app.get('/internal/mints')
@tracer.capture_method
def internal_list():
    return resource.list(app)


@app.post('/internal/mints')
@tracer.capture_method
def internal_create():
    return resource.create(app)


@app.put('/internal/mints/<id>')
@tracer.capture_method
def internal_update(id):
    return resource.update(app, id)


@app.post('/public/mints')
@tracer.capture_method
def public_create():
    return resource.create(app)


@app.get('/public/mints/<id>')
@tracer.capture_method
def public_get(id):
    return resource.get(app, id)


@app.put('/public/mints/<id>/fulfill')
@tracer.capture_method
def public_fulfill(id):
    return resource.fulfill(app, id)


@app.get('/v1/mints')
@tracer.capture_method
def list():
    return resource.list(app)


@app.post('/v1/mints')
@tracer.capture_method
def create():
    return resource.create(app)


@app.get('/v1/mints/<id>')
@tracer.capture_method
def get(id):
    return resource.get(app, id)


@app.put('/v1/mints/<id>')
@tracer.capture_method
def update(id):
    return resource.update(app, id)

# @app.get('/v1/mints/aggregate/search')
# @tracer.capture_method
# def search():
#     return resource.aggregate_search(app)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
