from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from ..utils.api import call_api
from ..utils.s3 import (get_image_key, get_image_url, get_max_token_id,
                        get_metadata_key, move_s3_object,
                        upload_metadata_to_s3)
from ..utils.tatum import Tatum

tracer = Tracer()
logger = Logger()
tatum = Tatum()


def to_hex(x):
    x = int(x)
    padding = 4
    return f"{x:#0{padding}x}"


def get_collection(id, organization):
    collection = call_api(
        method='GET',
        path='/collections/' + id,
        organization=organization
    )
    return collection


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    """Update product token metadata"""
    product = event.detail
    logger.info(product)

    # Check product data to see what we need to do
    collection_id = product['collection']
    organization_id = product['organization']
    token_id = product.get('token_id')

    # Get collection data
    collection = get_collection(collection_id, organization_id)
    contract_address = collection['contract_address']

    # Get token_id or create next one
    if not token_id:
        max_token_id = get_max_token_id(collection_id)
        token_id = max_token_id + 1
    token_id_hex = to_hex(token_id)
    logger.info({
        'contract_address': contract_address,
        'token_id': token_id,
        'token_id_hex': token_id_hex
    })

    # Move product image from /tmp to /metadata/collection_id/token_id
    old_key = '/'.join(product['image'].split('/')[-2:])
    metadata_key_dec = get_metadata_key(collection_id, token_id)
    metadata_key_hex = get_metadata_key(collection_id, token_id_hex)
    image_key = get_image_key(collection_id, token_id_hex)
    image_url = get_image_url(collection_id, token_id_hex)
    move_s3_object(old_key, image_key)

    # Upload product metadata to S3
    metadata = {
        'name': product['name'],
        'description': product['description'],
        'image': image_url,
        "attributes": product.get('properties', []),
        'external_url': 'https://versifylabs.com',
        # 'animation_url': '',
        # 'youtube_url': ''
    }
    upload_metadata_to_s3(metadata_key_dec, metadata)
    upload_metadata_to_s3(metadata_key_hex, metadata)

    # Save token to product
    response = call_api(
        method='PUT',
        path='/products/' + product['id'],
        body={
            'chain': collection.get('chain', 'polygon'),
            'contract_address': contract_address,
            'token_id': str(token_id),
            # 'metadata_url': metadata_url
        },
        organization=product['organization']
    )
    logger.info(response)

    return True
