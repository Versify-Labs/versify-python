from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..utils.mandrill import mailchimp

app = APIGatewayRestResolver(strip_prefixes=["/partners"])
logger = Logger()
tracer = Tracer()


@app.post("/mandrill/messages")
@tracer.capture_method
def create_message():
    payload = app.current_event.json_body
    response = mailchimp.messages.send_template(payload)
    return response


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
