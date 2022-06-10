from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)

from .service import Versify

logger = Logger()
tracer = Tracer()


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_campaign_send(event, context):
    campaign = event.detail
    versify = Versify(organization=campaign['organization'])
    versify.airdrops.create_from_campaign(campaign['id'])
    return True


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def on_airdrop_minted(event, context):
    txn = event.detail
    organization_id = event.detail['metadata']['organization']
    airdrop_id = event.detail['metadata']['airdrop']
    campaign_id = event.detail['metadata']['campaign']
    versify = Versify(organization_id)
    versify.airdrops.close(airdrop_id, txn)
    versify.campaigns.add_mint(campaign_id)
    return True
