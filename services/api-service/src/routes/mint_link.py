from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..resources import MintLink

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
resource = MintLink()


@app.get('/public/mint_links/<id>')
@tracer.capture_method
def public_get(id):
    return resource.get(app, id)


@app.get('/v1/mint_links')
@tracer.capture_method
def list():
    return resource.list(app)


@app.post('/v1/mint_links')
@tracer.capture_method
def create():
    return resource.create(app)


@app.get('/v1/mint_links/<id>')
@tracer.capture_method
def get(id):
    return resource.get(app, id)


@app.put('/v1/mint_links/<id>')
@tracer.capture_method
def update(id):
    return resource.update(app, id)


@app.delete('/v1/mint_links/<id>')
@tracer.capture_method
def delete(id):
    return resource.delete(app, id)


@app.put('/v1/mint_links/<id>/activate')
@tracer.capture_method
def activate(id):
    return resource.activate(app, id)


@app.put('/v1/mint_links/<id>/archive')
@tracer.capture_method
def archive(id):
    return resource.archive(app, id)


@app.put('/v1/mint_links/<id>/tag')
@tracer.capture_method
def tag(id):
    return resource.tag(app, id)


@app.get('/v1/mint_links/search')
@tracer.capture_method
def search_mint_links():
    return resource.search(app)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
