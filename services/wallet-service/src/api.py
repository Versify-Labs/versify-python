from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers
from versify.utilities.model import response

from .service import WalletService

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@tracer.capture_method
def sync(app):
    authorizer = app.current_event.request_context.authorizer
    email = authorizer.get('email')
    service = WalletService(email)
    service.sync_authorizer(authorizer)
    return service


@app.get("/wallet/profile")
@tracer.capture_method
def get_profile():
    service = sync(app)
    profile = service.get_profile()
    return response('get', profile.to_dict())


@app.get("/wallet/accounts")
@tracer.capture_method
def list_accounts():
    service = sync(app)
    accounts = service.list_accounts()
    data = [account.to_dict() for account in accounts]
    return response('list', data, 'account', '/accounts', False)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
