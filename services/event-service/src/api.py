import json
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities import parameters
from lambda_decorators import cors_headers

from .service import EventService

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

SECRET_NAME = os.environ['SECRET_NAME']
SECRET = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET)
AUTH0_WEBHOOK_SECRET = SECRET["AUTH0_WEBHOOK_SECRET"]


@app.post("/webhook/alchemy")
@tracer.capture_method
def alchemy_webhook():
    service = EventService()
    payload = app.current_event.json_body
    if payload.get('type') in ['ADDRESS_ACTIVITY']:
        event_data = payload['event']
        activities = event_data.get('activity', [])
        return service.process_blockchain_events(activities)
    return True


@app.post("/webhook/auth0")
@tracer.capture_method
def auth0_webhook():
    service = EventService()
    payload = app.current_event.json_body
    auth = app.current_event.get_header_value('Authorization')
    if auth != AUTH0_WEBHOOK_SECRET:
        logger.error('Invalid Authorization Header')
        return False
    logger.info(payload)
    logs = payload.get('logs', [])
    return service.process_auth_events(logs)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
