from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from lambda_decorators import cors_headers

from .processors.airdrop import AirdropProcessor
from .processors.billing import BillingProcessor
from .processors.transaction import TransactionProcessor
from .processors.usage import UsageProcessor
from .subscibers.slack import SlackSubscriber
from .subscibers.webhook import WebhookSubscriber
from .utils.eb import publish_event

app = APIGatewayRestResolver()
tracer = Tracer()
logger = Logger()


#########################
# Bus to Bus Connectors #
#########################


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def mongo_partner_connector(event, context):
    """Consume events from Mongo and publish to the PartnerBus"""
    detail_type = event.detail_type
    detail = event.detail
    event_bus = 'partner'
    source = 'mongo'
    publish_event(detail_type, detail, event_bus, source)
    return True

#############################
# Webhook to Bus Connectors #
#############################


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


######################
# Versify Publishers #
######################


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def partner_versify_connector(event, context):
    """Consume events from PartnerBus and pubish to the VersifyBus"""
    detail_type = event.detail_type
    detail = event.detail
    detail['id'] = event.detail.pop('_id')
    event_bus = 'versify'
    source = 'versify'
    publish_event(detail_type, detail, event_bus, source)
    return True


####################
# Event Processors #
####################


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def airdrop_processor(event, context):
    """When a new airdrop is created, mint tokens and notify contacts"""
    processor = AirdropProcessor(airdrop=event.detail)
    processor.start()
    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def billing_processor(event, context):
    """When a new stripe billing event is created, update internal systems"""
    processor = BillingProcessor(event.detail)
    processor.start()
    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def transaction_processor(event, context):
    """When a new blockchain transaction is created, update corresponding collection or mint"""
    processor = TransactionProcessor(txn=event.detail)
    processor.start()
    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def usage_processor(event, context):
    """When a new mint is created, add billing usage records"""
    processor = UsageProcessor(object=event.detail)
    processor.start()
    return True

#######################
# Versify Subscribers #
#######################


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def slack_subscriber(event, context):
    """Consume events and publish to Slack"""
    subscriber = SlackSubscriber()
    subscriber.start(event)
    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def webhook_subscriber(event, context):
    """Consume events and publish to matching webhooks"""
    subscriber = WebhookSubscriber()
    subscriber.start(event)
    return True


@cors_headers()
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def api(event, context):
    return app.resolve(event, context)
