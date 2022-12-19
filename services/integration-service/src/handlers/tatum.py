import time

from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from versify import Versify

from ..utils.tatum import Tatum

tracer = Tracer()
logger = Logger()
tatum = Tatum()
versify = Versify()


def match_collection(signature):

    collections = versify.collection_service.list({'signature': signature})
    logger.info(collections)

    if not collections or len(collections) < 1:
        logger.error('No matching collections for signature ', signature)
        return None

    return collections[0]


def match_mint(signature):
    mints = versify.mint_service.list({'signature': signature})
    logger.info(mints)

    if not mints or len(mints) < 1:
        logger.error('No matching mints for signature ', signature)
        return None

    return mints[0]


def update_collection(id, body, account):
    collection = versify.collection_service.update(
        id,
        body=body
    )
    logger.info(collection)

    if not collection:
        logger.error('Could not update collection')
        raise RuntimeError


def update_mint(id, body, account):
    mint = versify.mint_service.update(
        id,
        body=body
    )
    logger.info(mint)

    if not mint:
        logger.error('Could not update mint')
        raise RuntimeError


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    txn = event.detail
    sig_id = txn['signatureId']
    txn_id = txn['txId']
    sub_type = txn['subscriptionType']

    # Get details from Tatum
    txn_details = tatum.get_transaction_details(sig_id)
    logger.info(txn_details)
    if not txn_details:
        logger.error('Could not get transaction details')
        raise RuntimeError

    # Get collection with matching signature
    collection = match_collection(sig_id)
    if collection:
        collection_id = collection['id']
        account = collection['account']

        # Get deployed contract address from tatum
        contract_address = None
        retries_left = 10
        while not contract_address and retries_left > 0:
            tatum_txn = tatum.get_transaction(txn_id)
            logger.info(tatum_txn)

            if not tatum_txn:
                logger.error('Could not get transaction')
                raise RuntimeError

            contract_address = tatum_txn.get('contractAddress')
            retries_left -= 1
            time.sleep(1)

        if not contract_address:
            logger.error('Contract address could not be determined.')
            return False

        # Create update body based on tatum txn
        status = 'deployed' if sub_type == 'KMS_COMPLETED_TX' else 'failed'
        update_body = {
            'contract_address': contract_address,
            'status': status,
            'transaction': txn_id
        }

        # Save Updated Collection to DB
        update_collection(collection_id, update_body, account)
        return True

    # Get mint with matching signature
    mint = match_mint(sig_id)
    if mint:
        mint_id = mint['id']
        account = mint['account']

        # Create update body based on tatum txn
        status = 'complete' if sub_type == 'KMS_COMPLETED_TX' else 'failed'
        update_body = {
            'status': status,
            'transaction': txn_id
        }

        # Save Updated Mint to DB
        update_mint(mint_id, update_body, account)
        return True

    return True
