from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..services import (AccountService, AirdropService, CollectionService,
                        ContactService, MintLinkService, ProductService)

tracer = Tracer()
logger = Logger()
account_service = AccountService()
contact_service = ContactService()
collection_service = CollectionService()
product_service = ProductService(collection_service)
mint_link_service = MintLinkService(account_service)
airdrop_service = AirdropService(
    account_service, contact_service, mint_link_service, product_service)


def handle_product_archived(product):
    logger.info(product)

    # Archive all mint links for this product
    mint_links = mint_link_service.list(
        filter={
            'product': product['id']
        }
    )
    for mint_link in mint_links:
        mint_link_service.archive(mint_link['id'])

    # Archive all airdrops for this product
    airdrops = airdrop_service.list(
        filter={'product': product['id']}
    )
    for airdrop in airdrops:
        airdrop_service.archive(airdrop['id'])

    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    product = event.detail
    event_type = event.detail_type

    if event_type == 'product.archived':
        return handle_product_archived(product)

    return True
