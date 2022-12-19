from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

from versify import Versify
from versify.decorators import cors_headers, user_required

from ..errors import BadRequestError
from ..rest import CreateResponse, GetResponse, ListResponse, UserRequest

app = APIGatewayRestResolver(strip_prefixes=['/users'])
logger = Logger()
tracer = Tracer()
versify = Versify()


@app.post('/auth')
@tracer.capture_method
def authenticate_user():
    req = UserRequest(app)
    email = req.email
    user = versify.user_service.get(email)  # type: ignore
    return CreateResponse(req, user).json


@app.post('/accounts')
@tracer.capture_method
def create_account():
    req = UserRequest(app)
    body = req.body
    body['email'] = req.email
    account = versify.account_service.create(body)
    return CreateResponse(req, account).json


@app.post('/claims')
@tracer.capture_method
def create_claim():
    req = UserRequest(app)
    body = req.body
    body['email'] = req.email
    claim = versify.claim_service.create(body)
    return CreateResponse(req, claim).json


@app.get('/claims')
@tracer.capture_method
def list_claims():
    req = UserRequest(app)
    filter = req.filter
    filter['email'] = req.email
    limit = req.limit
    skip = req.skip
    count = versify.claim_service.count(req.filter)
    claims = versify.claim_service.list(filter, limit, skip)
    claims = versify.claim_service.expand(claims, req.expand_list)
    claims = claims.get('data', [])  # type: ignore
    return ListResponse(req, claims, count).json


@app.get('/claims/<id>')
@tracer.capture_method
def get_claim(id):
    req = UserRequest(app, id)
    claim = versify.claim_service.retrieve_by_id(id)
    claim = versify.claim_service.expand(claim, req.expand_list)
    return GetResponse(req, claim).json


@app.get('/events')
@tracer.capture_method
def list_events():
    req = UserRequest(app)
    filter = req.filter
    filter['email'] = req.email
    limit = req.limit
    skip = req.skip
    count = versify.event_service.count(req.filter)
    events = versify.event_service.list(filter, limit, skip)
    events = versify.event_service.expand(events, req.expand_list)
    events = events.get('data', [])  # type: ignore
    return ListResponse(req, events, count).json


@app.post('/mints')
@tracer.capture_method
def create_mint():
    req = UserRequest(app)
    body = req.body
    body['email'] = req.email
    mint = versify.mint_service.create(body)
    return CreateResponse(req, mint).json


@app.get('/mints')
@tracer.capture_method
def list_mints():
    req = UserRequest(app)
    filter = req.filter
    filter['email'] = req.email
    limit = req.limit
    skip = req.skip
    count = versify.mint_service.count(req.filter)
    mints = versify.mint_service.list(filter, limit, skip)
    mints = versify.mint_service.expand(mints, req.expand_list)
    mints = mints.get('data', [])  # type: ignore
    return ListResponse(req, mints, count).json


@app.get('/mints/<id>')
@tracer.capture_method
def get_mint(id):
    req = UserRequest(app, id)
    mint = versify.mint_service.retrieve_by_id(id)
    mint = versify.mint_service.expand(mint, req.expand_list)
    return GetResponse(req, mint).json


@app.post('/wallets')
@tracer.capture_method
def attach_wallet():
    req = UserRequest(app)
    body = req.body
    email = req.email
    address = body.get('address')
    type = body.get('type')
    if not address or not type or not email:
        raise BadRequestError('Missing required fields')
    user = versify.user_service.attach_wallet(email, address, type)
    return CreateResponse(req, user).json


@user_required
@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
