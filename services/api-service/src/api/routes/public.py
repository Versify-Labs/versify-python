from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.logging import correlation_paths

from versify import Versify
from versify.decorators import cors_headers

from ..rest import CreateResponse, GetResponse, ListResponse, PublicRequest

app = APIGatewayRestResolver(strip_prefixes=['/public'])
logger = Logger()
tracer = Tracer()
versify = Versify()


@app.get('/accounts/<id>')
@tracer.capture_method
def get_account(id):
    req = PublicRequest(app)
    account = versify.account_service.retrieve_by_id(id)
    if not account:
        raise NotFoundError('Account not found')
    branding = account.get('branding', {})
    branding['object'] = 'account'
    return GetResponse(req, branding).json


@app.get('/accounts/<id>/assets')
@tracer.capture_method
def get_account_assets(id):
    req = PublicRequest(app)
    filter = req.filter
    filter['account'] = id
    limit = req.limit
    skip = req.skip
    count = versify.product_service.count(req.filter)
    assets = versify.product_service.list(filter, limit, skip)
    assets = versify.product_service.expand(assets, req.expand_list)
    assets = assets.get('data', [])  # type: ignore
    return ListResponse(req, assets, count).json


@app.get('/accounts/<id>/branding')
@tracer.capture_method
def get_account_branding(id):
    req = PublicRequest(app)
    account = versify.account_service.retrieve_by_id(id)
    if not account:
        raise NotFoundError('Account not found')
    branding = account.get('branding', {})
    branding['object'] = 'account.branding'
    return GetResponse(req, branding).json


@app.post('/accounts/<id>/events')
@tracer.capture_method
def create_account_event(id):
    req = PublicRequest(app)
    body = req.body
    body['account'] = id
    event = versify.event_service.create(body)
    return CreateResponse(req, event).json


@app.get('/accounts/<id>/journeys')
@tracer.capture_method
def get_account_journeys(id):
    req = PublicRequest(app)
    filter = req.filter
    filter['account'] = id
    limit = req.limit
    skip = req.skip
    count = versify.journey_service.count(req.filter)
    journeys = versify.journey_service.list(filter, limit, skip)
    journeys = versify.journey_service.expand(journeys, req.expand_list)
    journeys = journeys.get('data', [])  # type: ignore
    return ListResponse(req, journeys, count).json


@app.get('/accounts/<id>/rewards')
@tracer.capture_method
def get_account_rewards(id):
    req = PublicRequest(app)
    filter = req.filter
    filter['account'] = id
    limit = req.limit
    skip = req.skip
    count = versify.reward_service.count(req.filter)
    rewards = versify.reward_service.list(filter, limit, skip)
    rewards = versify.reward_service.expand(rewards, req.expand_list)
    rewards = rewards.get('data', [])  # type: ignore
    return ListResponse(req, rewards, count).json


@app.get('/mint_links/<id>')
@tracer.capture_method
def get_mint_link(id):
    req = PublicRequest(app, id)
    link = versify.mint_link_service.retrieve_by_id(id)
    link = versify.mint_link_service.expand(link, req.expand_list)
    if not link:
        raise NotFoundError('Mint link not found')
    return GetResponse(req, link).json


@app.get('/signatures/<id>')
@tracer.capture_method
def get_signature(id):
    exists = versify.signature_service.exists(id)
    if not exists:
        raise NotFoundError('Signature not found')
    return True


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
