from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Webhook

app = APIGatewayRestResolver(strip_prefixes=["/v1"])
logger = Logger()
tracer = Tracer()
resource = Webhook()


@app.get('/webhooks')
@tracer.capture_method
def list_webhooks():
    return resource.list(app)


@app.post('/webhooks')
@tracer.capture_method
def create_webhooks():
    return resource.create(app)


@app.get('/webhooks/<id>')
@tracer.capture_method
def get_webhooks(id):
    return resource.get(app, id)


@app.put('/webhooks/<id>')
@tracer.capture_method
def update_webhooks(id):
    return resource.update(app, id)


@app.delete('/webhooks/<id>')
@tracer.capture_method
def delete_webhooks(id):
    return resource.delete(app, id)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
