from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers
from versify.utilities.model import response
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from .service import Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@tracer.capture_method
def sync(app):
    authorizer = app.current_event.request_context.authorizer
    email = authorizer.get('email')
    if not email:
        raise BadRequestError('Email is required for all wallet endpoints')
    service = Versify(email)
    return service


@app.post("/wallet/v1/accounts")
@tracer.capture_method
def create_account():
    versify = sync(app)
    payload = app.current_event.json_body
    account = versify.accounts.create(payload)
    return response('create', account)


@app.get("/wallet/v1/accounts")
@tracer.capture_method
def list_accounts():
    versify = sync(app)
    accounts = versify.accounts.list()
    return response('list', accounts, 'account', '/accounts', False)


@app.put("/wallet/v1/accounts/<account_id>")
@tracer.capture_method
def update_account(account_id):
    versify = sync(app)
    payload = app.current_event.json_body
    account = versify.accounts.update(account_id, payload)
    return response('update', account.to_dict())


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
