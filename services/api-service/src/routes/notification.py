from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Notification

app = APIGatewayRestResolver(strip_prefixes=["/v1"])
logger = Logger()
tracer = Tracer()
resource = Notification()


@app.get('/notifications')
@tracer.capture_method
def list_notifications():
    return resource.list(app)


@app.post('/notifications')
@tracer.capture_method
def create_notification():
    return resource.create(app)


@app.get('/notifications/<id>')
@tracer.capture_method
def get_notification(id):
    return resource.get(app, id)


@app.put('/notifications/<id>')
@tracer.capture_method
def update_notification(id):
    return resource.update(app, id)


@app.delete('/notifications/<id>')
@tracer.capture_method
def delete_notification(id):
    return resource.delete(app, id)


@app.get('/notifications/search')
@tracer.capture_method
def search_notifications():
    return resource.search(app)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
