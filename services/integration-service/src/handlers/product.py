from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from versify import Versify

tracer = Tracer()
logger = Logger()
versify = Versify()


def handle_product_updated(product):

    if product.get('archived', False):

        # Archive all airdrops for this product
        airdrops = versify.airdrop_service.list(
            filter={'product': product['_id']}
        )
        for airdrop in airdrops:
            versify.airdrop_service.archive(airdrop['id'])

        # Archive all mint links for this product
        mint_links = versify.mint_link_service.list(
            filter={'product': product['_id']}
        )
        for mint_link in mint_links:
            versify.mint_link_service.archive(mint_link['id'])

    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    product = event.detail
    event_type = event.detail_type

    if event_type == 'product.updated':
        return handle_product_updated(product)

    return True
