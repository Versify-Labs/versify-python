from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.api import call_api
from ..utils.tatum import Tatum

tracer = Tracer()
logger = Logger()
tatum = Tatum()


def match_collection(signature):
    response = call_api(
        method='GET',
        path='/collections',
        params={'signature': signature}
    )
    logger.info(response)

    collections = response.get('data')
    if not collections or len(collections) < 1:
        logger.error('No matching collections for signature ', signature)
        return None

    collection = collections[0]
    return collection


def match_mint(signature):
    response = call_api(
        method='GET',
        path='/mints',
        params={'signature': signature}
    )
    logger.info(response)

    mints = response.get('data')
    if not mints or len(mints) < 1:
        logger.error('No matching mints for signature ', signature)
        return None

    mint = mints[0]
    return mint


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    """Update collection based on txn"""
    txn = event.detail
    logger.info(txn)

    sig_id = txn['signatureId']
    txn_id = txn['txId']
    sub_type = txn['subscriptionType']
    status = 'complete' if sub_type == 'KMS_COMPLETED_TX' else 'failed'

    # Get details from Tatum
    txn_details = tatum.get_transaction_details(sig_id)
    logger.info(txn_details)

    # Get txn from tatum
    tatum_txn = tatum.get_transaction(txn_id)
    logger.info(tatum_txn)

    if not tatum_txn or not tatum_txn.get('transactionHash'):
        logger.error(tatum_txn)
        return

    # Get collection with matching signature
    collection = match_collection(sig_id)
    if collection:
        collection_id = collection['id']
        organization = collection['organization']

        # Create update body based on tatum txn
        update_body = {
            'status': status,
            'transaction': txn_id
        }
        if tatum_txn.get('contractAddress'):
            update_body['contract_address'] = tatum_txn.get('contractAddress')

        # Save Updated Collection to DB
        response = call_api(
            method='PUT',
            path=f'/collections/{collection_id}',
            body=update_body,
            organization=organization
        )
        logger.info(response)

    # Get mint with matching signature
    mint = match_mint(sig_id)
    if mint:
        mint_id = mint['id']
        organization = mint['organization']

        # Create update body based on tatum txn
        update_body = {
            'status': status,
            'transaction': txn_id
        }

        # Save Updated Mint to DB
        response = call_api(
            method='PUT',
            path=f'/mints/{mint_id}',
            body=update_body,
            organization=organization
        )
        logger.info(response)

    return True
