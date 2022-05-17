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


@app.get("/wallet/ping")
@tracer.capture_method
def ping():
    return response('get', True)


@app.get("/wallet/me")
@tracer.capture_method
def get_wallet():
    service = sync(app)
    wallet = service.get_wallet()
    return response('get', wallet.to_dict())


@app.get("/wallet/blockchain_addresses")
@tracer.capture_method
def list_blockchain_addresses():
    service = sync(app)
    blockchain_addresses = service.list_blockchain_addresses()
    data = [blockchain_address.to_dict()
            for blockchain_address in blockchain_addresses]
    return response('list', data, 'blockchain_address', '/blockchain_addresses', False)


@app.get("/backend/wallets/<id>/blockchain_addresses")
@tracer.capture_method
def validate_blockchain_addresses(id):
    service = WalletService(id)
    blockchain_addresses = service.list_blockchain_addresses()
    data = [blockchain_address.to_dict()
            for blockchain_address in blockchain_addresses]
    return response('list', data, 'blockchain_address', '/blockchain_addresses', False)


@app.put("/wallet/blockchain_addresses/<id>")
@tracer.capture_method
def update_blockchain_address(id):
    service = sync(app)
    payload = app.current_event.json_body
    blockchain_address = service.update_blockchain_address(
        id, payload['description'])
    return response('update', blockchain_address.to_dict())


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
