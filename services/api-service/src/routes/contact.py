from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import Contact

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
resource = Contact()


@app.get('/internal/contacts/aggregate/search')
@tracer.capture_method
def internal_aggregate_search():
    return resource.aggregate_search(app)


@app.get('/internal/contacts/aggregate/segment')
@tracer.capture_method
def internal_aggregate_segment():
    return resource.aggregate_segment(app)


@app.post('/public/contacts')
@tracer.capture_method
def public_create():
    return resource.create(app)


@app.get('/v1/contacts')
@tracer.capture_method
def list():
    return resource.list(app)


@app.post('/v1/contacts')
@tracer.capture_method
def create():
    return resource.create(app)


@app.get('/v1/contacts/<id>')
@tracer.capture_method
def get(id):
    return resource.get(app, id)


@app.put('/v1/contacts/<id>')
@tracer.capture_method
def update(id):
    return resource.update(app, id)


@app.delete('/v1/contacts/<id>')
@tracer.capture_method
def delete(id):
    return resource.delete(app, id)


@app.put('/v1/contacts/<id>/activate')
@tracer.capture_method
def activate(id):
    return resource.activate(app, id)


@app.put('/v1/contacts/<id>/archive')
@tracer.capture_method
def archive(id):
    return resource.archive(app, id)


@app.put('/v1/contacts/<id>/tag')
@tracer.capture_method
def tag(id):
    return resource.tag(app, id)


@app.get('/v1/contacts/aggregate/search')
@tracer.capture_method
def aggregate_search():
    return resource.aggregate_search(app)


@app.get('/v1/contacts/aggregate/segment')
@tracer.capture_method
def aggregate_segment():
    return resource.aggregate_segment(app)


@app.get('/v1/contacts/aggregate/tags')
@tracer.capture_method
def aggregate_tags():
    return resource.aggregate_tags(app)


@cors_headers
# type: ignore
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
