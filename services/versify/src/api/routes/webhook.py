from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ...utils.eb import publish_event

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()


####################
# Partner Webhooks #
####################


@app.post("/webhook/alchemy")
@tracer.capture_method
def alchemy_partner_connector():
    """Consume events from Alchemy and pubish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = 'transaction.created'
    detail = payload
    event_bus = 'partner'
    source = 'alchemy'
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@app.post("/webhook/stripe")
@tracer.capture_method
def stripe_partner_connector():
    """Consume events from Stripe and pubish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = 'event.created'
    detail = payload
    event_bus = 'partner'
    source = 'stripe'
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@app.post("/webhook/tatum")
@tracer.capture_method
def tatum_partner_connector():
    """Consume events from Tatum and pubish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = 'transaction.created'
    detail = payload
    event_bus = 'partner'
    source = 'tatum'
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
