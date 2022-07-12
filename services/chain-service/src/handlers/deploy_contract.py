import json
import os

from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.api import call_api
from ..utils.tatum import Tatum

ENV = os.environ['ENVIRONMENT']
METADATA_BUCKET = f"cdn{'-dev' if ENV == 'dev' else ''}.versifylabs.com"
METADATA_URI_BASE = f"https://cdn{'-dev' if ENV == 'dev' else ''}.versifylabs.com"
SECRET_NAME = os.environ['SECRET_NAME']
SECRET = json.loads(parameters.get_secret(SECRET_NAME))  # type: ignore

tracer = Tracer()
logger = Logger()
tatum = Tatum()


def get_contract_token_uri(collection_id):
    return f"{METADATA_URI_BASE}/products/{collection_id}" + "/{id}.json"


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    """Deploy a new ERC1155 contract for the collection"""
    collection = event.detail
    collection_id = collection['id']
    org_id = collection['organization']

    # Create token URI
    token_uri = get_contract_token_uri(collection_id)

    # Deploy contract
    response = tatum.deploy_contract(token_uri)
    logger.info(response)
    signature_id = response.get('signatureId')
    if not signature_id:
        logger.error(response)
        raise RuntimeError

    # Save transaction with collection
    response = call_api(
        method='PUT',
        path=f'/collections/{collection_id}',
        body={
            'signature': signature_id,
            'uri': token_uri
        },
        organization=org_id
    )
    logger.info(response)
    if not response:
        logger.error(response)
        raise RuntimeError

    return True
