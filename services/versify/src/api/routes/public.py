from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ...services import (AccountService, AirdropService, CollectionService,
                         ContactService, EventService, MintLinkService,
                         MintService, NoteService, ProductService,
                         SignatureService, UserService, WebhookService)
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
note_service = NoteService()
signature_service = SignatureService(collection_service, mint_service)
webhook_service = WebhookService()


@app.get('/public/mint_links/<id>')
@tracer.capture_method
def get_mint_link(id):
    req = Request(app, id)
    mint_link = mint_link_service.retrieve_by_id(id)
    mint_link = mint_link_service.expand(mint_link, req.expand_list)
    return Response(req, mint_link).get


@app.get('/public/signatures/<id>')
@tracer.capture_method
def get_signature(id):
    return signature_service.exists(id)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
