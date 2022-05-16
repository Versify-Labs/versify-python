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

# @app.post("/dashboard/events")
# @tracer.capture_method
# def create_event():
#     service = EventService()
#     payload = app.current_event.json_body
#     detail_type = payload['detail_type']
#     detail = payload['detail']
#     source = payload['source']
#     return service.publish_event(detail_type, detail, source)


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

# @app.post("/webhook/contentful")
# @tracer.capture_method
# def contentful_webhook():
#     service = EventService()
#     topic = app.current_event.get_header_value('X-Contentful-Topic')
#     _, resource, action = topic.split('.')
#     detail_type = f'{resource}.{action}'.lower()
#     detail = app.current_event.json_body
#     source = 'contentful'
#     return service.publish_event(detail_type, detail, source)


# @app.post("/webhook/stripe")
# @tracer.capture_method
# def stripe_webhook():
#     service = EventService()
#     signature = app.current_event.get_header_value("Stripe-Signature")
#     payload = app.current_event.raw_event['body']
#     wh_secret = SECRET['STRIPE_PLATFORM_WEBHOOK_SECRET']
#     detail_type = ''
#     detail = {}
#     source = 'stripe'
#     try:
#         event = stripe.Webhook.construct_event(payload, signature, wh_secret)
#         detail_type = event['type']
#         detail = event['data']['object']
#     except ValueError as e:
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         raise e
#     return service.publish_event(detail_type, detail, source)


# @app.post("/webhook/stripe_connect")
# @tracer.capture_method
# def stripe_connect_webhook():
#     service = EventService()
#     signature = app.current_event.get_header_value("Stripe-Signature")
#     payload = app.current_event.raw_event['body']
#     wh_secret = SECRET['STRIPE_CONNECT_WEBHOOK_SECRET']
#     detail_type = ''
#     detail = {}
#     source = 'stripe'
#     try:
#         event = stripe.Webhook.construct_event(payload, signature, wh_secret)
#         detail_type = event['type']
#         detail = event['data']['object']
#     except ValueError as e:
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         raise e
#     return service.publish_event(detail_type, detail, source)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
