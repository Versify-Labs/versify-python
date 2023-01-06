from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

from versify import Versify
from versify.decorators import cors_headers

from ...utils.eb import publish_event

app = APIGatewayRestResolver(strip_prefixes=["/webhook"])
logger = Logger()
tracer = Tracer()
versify = Versify()


@app.post("/alchemy")
@tracer.capture_method
def alchemy_partner_connector():
    """Consume events from Alchemy and publish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = "transaction.created"
    detail = payload
    event_bus = "partner"
    source = "alchemy"
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@app.post("/stripe")
@tracer.capture_method
def stripe_partner_connector():
    """Consume events from Stripe and publish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = "event.created"
    detail = payload
    event_bus = "partner"
    source = "stripe"
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@app.post("/tatum")
@tracer.capture_method
def tatum_partner_connector():
    """Consume events from Tatum and publish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = "transaction.created"
    detail = payload
    event_bus = "partner"
    source = "tatum"
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@cors_headers
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
