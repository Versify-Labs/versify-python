from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from versify.utilities.model import response

from .service import Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_airdrop(event, context):
    airdrop = event.detail
    versify = Versify(organization=airdrop['organization'])
    order = versify.orders.create_order_from_airdrop(airdrop)
    return response('create', order)


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_fulfillment(event, context):
    fulfillment = event.detail
    versify = Versify(fulfillment['email'], fulfillment['organization'])
    order = versify.orders.update_order_with_fulfillment(fulfillment)
    return response('create', order)


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_token_minted(event, context):
    transaction = event.detail
    versify = Versify(organization=transaction['metadata']['organization'])
    fulfillment = versify.fulfillments.update_with_txn(transaction)
    return response('update', fulfillment)


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_wallet_update(event, context):
    wallet = event.detail
    versify = Versify(email=wallet['email'])

    # Get unfulfilled orders for email
    query = {'fulfillment_status': 'unfulfilled'}
    unfulfilled_orders = versify.orders.list_by_email(query)
    logger.info(unfulfilled_orders)

    # fulfill them
    for order in unfulfilled_orders:
        order_id = order['id']
        order_update_body = {'fulfillment_status': 'pending'}
        versify.orders.update(order_id, order_update_body)
        fulfillment = versify.fulfillments.create(order_id, {})
        logger.info(fulfillment)

    return True
