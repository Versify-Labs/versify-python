from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Airdrop

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
resource = Airdrop()


@app.put('/internal/airdrops/<id>')
@tracer.capture_method
def internal_update(id):
    return resource.update(app, id)


@app.get('/v1/airdrops')
@tracer.capture_method
def list():
    return resource.list(app)


@app.post('/v1/airdrops')
@tracer.capture_method
def create():
    return resource.create(app)


@app.get('/v1/airdrops/<id>')
@tracer.capture_method
def get(id):
    return resource.get(app, id)


@app.put('/v1/airdrops/<id>')
@tracer.capture_method
def update(id):
    return resource.update(app, id)


@app.put('/v1/airdrops/<id>/send')
@tracer.capture_method
def send(id):
    return resource.send(app, id)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
