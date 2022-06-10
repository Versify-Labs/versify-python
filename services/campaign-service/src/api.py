from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers
from versify.utilities.model import response

from .service import Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@tracer.capture_method
def sync(app):
    organization = app.current_event.get_header_value('X-Organization')
    versify = Versify(organization)
    return versify


"""
Airdrop Endpoints
"""


@app.get("/campaign/v1/airdrops")
@tracer.capture_method
def list_airdrops():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters or {}
    airdrops = versify.airdrops.list_by_org(query_params)
    return response('list', airdrops, 'airdrop', '/airdrops', False)


@app.post("/campaign/v1/airdrops")
@tracer.capture_method
def create_airdrop():
    return 'Not implemented'


@app.delete("/campaign/v1/airdrops/<airdrop_id>")
@tracer.capture_method
def delete_airdrop(airdrop_id):
    return 'Not implemented'


@app.get("/campaign/v1/airdrops/<airdrop_id>")
@tracer.capture_method
def get_airdrop(airdrop_id):
    versify = sync(app)
    campaign = versify.airdrops.get(airdrop_id)
    return response('get', campaign)


@app.put("/campaign/v1/airdrops/<airdrop_id>")
@tracer.capture_method
def update_airdrop(airdrop_id):
    return 'Not implemented'


@app.put("/campaign/v1/airdrops/<airdrop_id>/actions/fulfill")
@tracer.capture_method
def fulfill_airdrop(airdrop_id):
    versify = sync(app)
    payload = app.current_event.json_body
    airdrop = versify.airdrops.fulfill(airdrop_id, payload)
    return response('update', airdrop)


"""
Campaign Endpoints
"""


@app.get("/campaign/v1/campaigns")
@tracer.capture_method
def list_campaigns():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters or {}
    campaigns = versify.campaigns.list_by_org(query_params)
    return response('list', campaigns, 'campaign', '/campaigns', False)


@app.post("/campaign/v1/campaigns")
@tracer.capture_method
def create_campaign():
    versify = sync(app)
    payload = app.current_event.json_body
    campaign = versify.campaigns.create(payload)
    return response('create', campaign)


@app.delete("/campaign/v1/campaigns/<campaign_id>")
@tracer.capture_method
def delete_campaign(campaign_id):
    return 'Not implemented'


@app.get("/campaign/v1/campaigns/<campaign_id>")
@tracer.capture_method
def get_campaign(campaign_id):
    versify = sync(app)
    campaign = versify.campaigns.get(campaign_id)
    return response('get', campaign)


@app.put("/campaign/v1/campaigns/<campaign_id>")
@tracer.capture_method
def update_campaign(campaign_id):
    versify = sync(app)
    payload = app.current_event.json_body
    campaign = versify.campaigns.update(campaign_id, payload)
    return response('update', campaign)


@app.put("/campaign/v1/campaigns/<campaign_id>/actions/send")
@tracer.capture_method
def send_campaign(campaign_id):
    versify = sync(app)
    campaign = versify.campaigns.send(campaign_id)
    return response('update', campaign)


@app.get("/campaign/v1/campaigns/<campaign_id>/airdrops")
@tracer.capture_method
def list_campaign_airdrops(campaign_id):
    versify = sync(app)
    query_params = app.current_event.query_string_parameters or {}
    airdrops = versify.airdrops.list_by_campaign(campaign_id, query_params)
    return response('list', airdrops, 'airdrop', '/campaigns/{campaign_in}/airdrops', False)


@app.get("/campaign/v1/campaigns/<campaign_id>/claims")
@tracer.capture_method
def list_campaign_claims(campaign_id):
    versify = sync(app)
    query_params = app.current_event.query_string_parameters or {}
    claims = versify.claims.list_by_campaign(campaign_id, query_params)
    return response('list', claims, 'claim', '/campaigns/{campaign_in}/claims', False)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
