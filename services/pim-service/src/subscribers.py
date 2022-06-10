from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from .service import Versify

tracer = Tracer()
logger = Logger()


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_contract_deployed(event, context):
    organization_id = event.detail['metadata']['organization']
    collection_id = event.detail['metadata']['collection']
    contract_address = event.detail['contract_address']
    versify = Versify(organization_id)
    versify.collections.update_with_contract(
        id=collection_id,
        contract=contract_address
    )
    return True


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_airdrop_created(event, context):
    airdrop = event.detail
    product_id = airdrop['product']
    organization_id = airdrop['organization']
    versify = Versify(organization_id)
    versify.products.add_airdrop(product_id)
    return True


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_order_created(event, context):
    organization = event.detail['organization']
    versify = Versify(organization)
    versify.products.update_with_order(order=event.detail)
    return True
