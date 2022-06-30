from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Wallet

app = APIGatewayRestResolver(strip_prefixes=["/v1"])
logger = Logger()
tracer = Tracer()
resource = Wallet()


@app.post('/wallets')
@tracer.capture_method
def create():
    return resource.create(app)


@app.post('/wallets')
@tracer.capture_method
def list():
    return resource.create(app)


@app.get('/wallets/<id>')
@tracer.capture_method
def get(id):
    return resource.get(app, id)


@app.put('/wallets/<id>')
@tracer.capture_method
def update(id):
    return resource.update(app, id)


@app.put('/wallets/<id>/accounts')
@tracer.capture_method
def attach_account(id):
    return resource.attach_account(app, id)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
