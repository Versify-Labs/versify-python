from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Note

app = APIGatewayRestResolver(strip_prefixes=["/v1"])
logger = Logger()
tracer = Tracer()
resource = Note()


@app.get('/notes')
@tracer.capture_method
def list_notes():
    return resource.list(app)


@app.post('/notes')
@tracer.capture_method
def create_note():
    return resource.create(app)


@app.get('/notes/<id>')
@tracer.capture_method
def get_note(id):
    return resource.get(app, id)


@app.put('/notes/<id>')
@tracer.capture_method
def update_note(id):
    return resource.update(app, id)


@app.delete('/notes/<id>')
@tracer.capture_method
def delete_note(id):
    return resource.delete(app, id)


@app.get('/notes/search')
@tracer.capture_method
def search_notes():
    return resource.search(app)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
