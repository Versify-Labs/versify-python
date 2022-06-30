from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Event

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
resource = Event()


@app.post('/internal/events')
@tracer.capture_method
def internal_create():
    return resource.create(app)


@app.get('/v1/events')
@tracer.capture_method
def list():
    return resource.list(app)


@app.post('/v1/events')
@tracer.capture_method
def create():
    return resource.create(app)


@app.get('/v1/events/<id>')
@tracer.capture_method
def get(id):
    return resource.get(app, id)


@app.get('/v1/events/search')
@tracer.capture_method
def search():
    return resource.search(app)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
