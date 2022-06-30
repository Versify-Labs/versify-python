from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.api import call_api
from ..utils.tatum import Tatum

tracer = Tracer()
logger = Logger()
tatum = Tatum()


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    """Mint a token to the collections contract"""
    mint = event.detail
    logger.info(mint)

    # Get the product being minted
    product = call_api(
        method='GET',
        path='/products/' + mint['product'],
        params={
            'expand': 'collection'
        }
    )

    # Mint token to contract
    response = tatum.mint_token(
        contract=product['collection']['contract_address'],
        token=product['token_id'],
        to=mint['wallet_address']
    )
    logger.info(response)

    # Save transaction with mint
    signature_id = response.get('signatureId')
    if not signature_id:
        logger.error(response)
        return False

    response = call_api(
        method='PUT',
        path='/mints/' + mint['_id'],
        body={
            'signature': signature_id
        },
        organization=mint['organization']
    )
    logger.info(response)

    return True
