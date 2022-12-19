from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from versify import Versify

tracer = Tracer()
logger = Logger()
versify = Versify()


def handle_claim_created(claim: dict) -> bool:
    """Send a claim.created event to the event service.

    Args:
        claim (dict): The claim object.

    Returns:
        bool: True if successful.
    """

    # Create activity for customer that created the claim
    body = {
        'account': claim['account'],
        'contact': claim['contact'],
        'source': 'versify',
        'detail_type': 'claim.created',
        'detail': claim
    }
    versify.event_service.create(body)

    return True


def handle_claim_updated(claim):
    logger.info(claim)
    return True


def handle_claim_deleted(claim):
    logger.info(claim)
    return True


@event_source(data_class=EventBridgeEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):
    claim = event.detail
    event_type = event.detail_type

    if event_type == 'claim.created':
        return handle_claim_created(claim)
    if event_type == 'claim.updated':
        return handle_claim_updated(claim)
    if event_type == 'claim.deleted':
        return handle_claim_deleted(claim)

    return True
