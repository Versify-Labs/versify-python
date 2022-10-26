from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ...services import (AccountService, AirdropService, CollectionService,
                         ContactService, EventService, MintLinkService,
                         MintService, ProductService, UserService)
from ..rest import Request, Response

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()

account_service = AccountService()
collection_service = CollectionService()
contact_service = ContactService()
event_service = EventService()
mint_link_service = MintLinkService(account_service)
product_service = ProductService(collection_service)
airdrop_service = AirdropService(account_service, contact_service, mint_link_service, product_service)
user_service = UserService(account_service)
mint_service = MintService(airdrop_service, contact_service, mint_link_service, user_service)


@app.post('/users/auth')
@tracer.capture_method
def authenticate_user():
    req = Request(app)
    user_id = req.user
    user = user_service.retrieve_by_id(user_id)  # type: ignore
    return Response(req, user).create


@app.post('/users/accounts')
@tracer.capture_method
def create_account():
    req = Request(app)
    body = req.body
    body['email'] = req.email
    account = account_service.create(body)
    return Response(req, account).create


@app.get('/users/events')
@tracer.capture_method
def list_events():
    req = Request(app)
    filter = req.filter
    filter['email'] = req.email
    limit = req.limit
    skip = req.skip
    events = event_service.list(filter, limit, skip)
    events = event_service.expand(events, req.expand_list)
    events = events.get('data', [])  # type: ignore
    count = event_service.count(req.filter)
    return Response(req, events, count).list


@app.post('/users/mints')
@tracer.capture_method
def create_mint():
    req = Request(app)
    body = req.body
    body['email'] = req.email
    mint = mint_service.create(body)
    return Response(req, mint).create


@app.get('/users/mints')
@tracer.capture_method
def list_mints():
    req = Request(app)
    filter = req.filter
    filter['email'] = req.email
    limit = req.limit
    skip = req.skip
    mints = mint_service.list(filter, limit, skip)
    mints = mint_service.expand(mints, req.expand_list)
    mints = mints.get('data', [])  # type: ignore
    count = mint_service.count(req.filter)
    return Response(req, mints, count).list


@app.get('/users/mints/<id>')
@tracer.capture_method
def get_mint(id):
    req = Request(app, id)
    mint = mint_service.retrieve_by_id(id)
    mint = mint_service.expand(mint, req.expand_list)
    return Response(req, mint).get


@app.put('/users/mints/<id>/fulfill')
@tracer.capture_method
def fulfill_mint(id):
    req = Request(app, id)
    wallet_address = req.body['wallet_address']
    mint = mint_service.fulfill(id, wallet_address)
    return Response(req, mint).update


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
