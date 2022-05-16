from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from .service import Tatum, Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()
tatum = Tatum()
versify = Versify()


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_blockchain_transaction(event, context):
    """Sync internal table with blockchain transactions"""

    # List all pending transactions
    pending_signatures = versify.signatures.list_by_status('pending')

    # For each pending transaction
    for sig in pending_signatures:
        logger.info(sig)

        sig_id = sig['id']
        sig_metadata = sig['metadata']

        # Get details from Tatum
        txn_details = tatum.get_transaction_details(sig_id)
        logger.info(txn_details)

        # If complete, mark as such in db and create transaction
        if txn_details.get('txId', None):
            txn_id = txn_details['txId']

            # Get txn from tatum
            tatum_txn = tatum.get_transaction(txn_id)
            logger.info(tatum_txn)

            if not tatum_txn or not tatum_txn.get('transactionHash'):
                logger.error(tatum_txn)
                continue

            # Create txn in db
            txn_body = versify.transactions.convert_tatum_txn(tatum_txn)
            txn_body['metadata'] = sig_metadata
            txn_body['signature'] = sig_id
            logger.info(txn_body)

            txn = versify.transactions.create(txn_id, txn_body)
            logger.info(txn)

            # Mark signature as complete and add txn id
            update_body = {
                'status': 'complete',
                'transaction': txn['id']
            }
            versify.signatures.update(sig_id, update_body)

    return True


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_collection_created(event, context):
    """Deploy a new ERC1155 contract for the collection"""
    collection = event.detail
    logger.info(collection)

    token_uri = collection['token_uri']

    response = tatum.deploy_contract(token_uri)
    logger.info(response)

    signature_id = response.get('signatureId')
    if not signature_id:
        logger.error(response)
        return False

    try:
        payload = {
            'metadata': {
                'type': 'DeployContract',
                'collection': collection['id'],
                'organization': collection['organization']
            }
        }
        sig = versify.signatures.create(signature_id, payload)
        logger.info(sig)
    except:
        logger.error('Error creating signature')
        return True

    return True


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_fulfillment_created(event, context):
    """Mint a token to the collections contract"""
    fulfillment = event.detail
    logger.info(fulfillment)

    to = fulfillment['blockchain_address']
    items = fulfillment['items']

    for item in items:
        product = item['product_details']
        contract = product['contract_address']
        token = product['token_id']

        response = tatum.mint_token(contract, token, to)
        logger.info(response)

        signature_id = response.get('signatureId')
        if not signature_id:
            logger.error(response)
            return False

        try:
            payload = {
                'metadata': {
                    'type': 'MintToken',
                    'collection': product['collection'],
                    'fulfillment': fulfillment['id'],
                    'order': fulfillment['order'],
                    'organization': product['organization'],
                    'product': product['id'],
                }
            }
            sig = versify.signatures.create(signature_id, payload)
            logger.info(sig)
        except:
            logger.error('Error creating signature')
            continue

    return True
