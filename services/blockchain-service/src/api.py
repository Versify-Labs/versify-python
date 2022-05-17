from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from .service import Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@app.get("/backend/signatures/<id>")
@tracer.capture_method
def get_signature(id):
    versify = Versify()
    signature = versify.signatures.get(id)
    if signature:
        return True
    else:
        raise NotFoundError


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
