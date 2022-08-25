from enum import Enum

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..api.errors import BadRequestError
from ..services import (AccountService, AirdropService, CollectionService,
                        ContactService, EventService, MintLinkService,
                        MintService, NoteService, ProductService,
                        SignatureService, UserService, WebhookService)
from ..utils.eb import publish_event
from .rest import Request, Response

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()

account_service = AccountService()
collection_service = CollectionService()
contact_service = ContactService()
event_service = EventService()
mint_link_service = MintLinkService(account_service)
product_service = ProductService(collection_service)
airdrop_service = AirdropService(
    account_service, contact_service, mint_link_service, product_service)
mint_service = MintService(airdrop_service, contact_service, mint_link_service)
note_service = NoteService()
signature_service = SignatureService(collection_service, mint_service)
user_service = UserService(account_service)
webhook_service = WebhookService()


############
# Accounts #
############


@app.post('/.+/accounts')
@tracer.capture_method
def create_account():
    req = Request(app)
    body = req.body
    body['email'] = req.email
    account = account_service.create(body)
    return Response(req, account).create


@app.get('/.+/accounts/<id>')
@tracer.capture_method
def get_account(id):
    req = Request(app, id)
    account = account_service.retrieve_by_id(id)
    return Response(req, account).get


@app.put('/.+/accounts/<id>')
@tracer.capture_method
def update_account(id):
    req = Request(app, id)
    account = account_service.update(id, req.body)
    return Response(req, account).update


####################
# Account Sessions #
####################


@app.post('/.+/accounts/<id>/billing')
@tracer.capture_method
def create_billing_session(id):
    req = Request(app, id)
    checkout = account_service.create_billing_session(id)
    return Response(req, checkout).create


@app.post('/.+/accounts/<id>/checkout')
@tracer.capture_method
def create_checkout_session(id):
    req = Request(app, id)
    checkout = account_service.create_checkout_session(id)
    return Response(req, checkout).create


###################
# Account Members #
###################


@app.post('/.+/accounts/<id>/members')
@tracer.capture_method
def create_account_member(id):
    req = Request(app, id)
    body = req.body
    body['account'] = req.account
    member = account_service.create_member(id, body)
    return Response(req, member).create


@app.get('/.+/accounts/<id>/members')
@tracer.capture_method
def list_account_members(id):
    req = Request(app, id)
    account_id = req.account or id
    members = account_service.list_members(account_id)
    return Response(req, members).list


####################
# Account Invoices #
####################


@app.get('/.+/accounts/<id>/invoices')
@tracer.capture_method
def list_account_invoices(id):
    req = Request(app, id)
    account_id = req.account or id
    invoices = account_service.list_invoices(account_id)
    return Response(req, invoices).list


#########################
# Account Subscriptions #
#########################


@app.get('/.+/accounts/<id>/subscriptions')
@tracer.capture_method
def list_account_subscriptions(id):
    req = Request(app, id)
    account_id = req.account or id
    subscriptions = account_service.list_subscriptions(account_id)
    return Response(req, subscriptions).list


############
# Airdrops #
############


@app.post('/.+/airdrops')
@tracer.capture_method
def create_airdrop():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    airdrop = airdrop_service.create(body)
    return Response(req, airdrop).create


@app.get('/.+/airdrops')
@tracer.capture_method
def list_airdrops():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    airdrops = airdrop_service.list(filter, limit, skip)
    airdrops = airdrop_service.expand(airdrops, req.expand_list)
    airdrops = airdrops.get('data', [])  # type: ignore
    count = airdrop_service.count(req.filter)
    return Response(req, airdrops, count).list


@app.get('/.+/airdrops/<id>')
@tracer.capture_method
def get_airdrop(id):
    req = Request(app, id)
    airdrop = airdrop_service.retrieve_by_id(id)
    airdrop = airdrop_service.expand(airdrop, req.expand_list)
    return Response(req, airdrop).get


@app.put('/.+/airdrops/<id>')
@tracer.capture_method
def update_airdrop(id):
    req = Request(app, id)
    airdrop = airdrop_service.update(id, req.body)
    return Response(req, airdrop).update


@app.delete('/.+/airdrops/<id>')
@tracer.capture_method
def delete_airdrop(id):
    req = Request(app, id)
    airdrop = airdrop_service.delete(id)
    return Response(req, airdrop).update


@app.put('/.+/airdrops/<id>/send')
@tracer.capture_method
def send_airdrop(id):
    req = Request(app, id)
    airdrop = airdrop_service.send(id)
    return Response(req, airdrop).update


###############
# Collections #
###############


@app.post('/.+/collections')
@tracer.capture_method
def create_collection():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    collection = collection_service.create(body)
    return Response(req, collection).create


@app.get('/.+/collections')
@tracer.capture_method
def list_collections():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    collections = collection_service.list(filter, limit, skip)
    collections = collection_service.expand(collections, req.expand_list)
    collections = collections.get('data', [])  # type: ignore
    count = collection_service.count(req.filter)
    return Response(req, collections, count).list


@app.get('/.+/collections/<id>')
@tracer.capture_method
def get_collection(id):
    req = Request(app, id)
    collection = collection_service.retrieve(id)
    collection = collection_service.expand(collection, req.expand_list)
    return Response(req, collection).get


@app.put('/.+/collections/<id>')
@tracer.capture_method
def update_collection(id):
    req = Request(app, id)
    collection = collection_service.update(id, req.body)
    return Response(req, collection).update


@app.delete('/.+/collections/<id>')
@tracer.capture_method
def delete_collection(id):
    req = Request(app, id)
    collection = collection_service.delete(id)
    return Response(req, collection).update


############
# Contacts #
############


@app.post('/.+/contacts')
@tracer.capture_method
def create_contact():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    contact = contact_service.create(body)
    return Response(req, contact).create


@app.get('/.+/contacts')
@tracer.capture_method
def list_contacts():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    contacts = contact_service.list(filter, limit, skip)
    contacts = contact_service.expand(contacts, req.expand_list)
    contacts = contacts.get('data', [])  # type: ignore
    count = contact_service.count(req.filter)
    return Response(req, contacts, count).list


@app.get('/.+/contacts/<id>')
@tracer.capture_method
def get_contact(id):
    req = Request(app, id)
    contact = contact_service.retrieve_by_id(id)
    contact = contact_service.expand(contact, req.expand_list)
    return Response(req, contact).get


@app.put('/.+/contacts/<id>')
@tracer.capture_method
def update_contact(id):
    req = Request(app, id)
    contact = contact_service.update(id, req.body)
    return Response(req, contact).update


@app.delete('/.+/contacts/<id>')
@tracer.capture_method
def delete_contact(id):
    req = Request(app, id)
    contact = contact_service.delete(id)
    return Response(req, contact).update


##########
# Events #
##########


@app.post('/.+/events')
@tracer.capture_method
def create_event():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    event = event_service.create(body)
    return Response(req, event).create


@app.get('/.+/events')
@tracer.capture_method
def list_events():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    events = event_service.list(filter, limit, skip)
    events = event_service.expand(events, req.expand_list)
    events = events.get('data', [])  # type: ignore
    count = event_service.count(req.filter)
    return Response(req, events, count).list


@app.get('/.+/events/<id>')
@tracer.capture_method
def get_event(id):
    req = Request(app, id)
    event = event_service.retrieve_by_id(id)
    event = event_service.expand(event, req.expand_list)
    return Response(req, event).get


@app.delete('/.+/events/<id>')
@tracer.capture_method
def delete_event(id):
    req = Request(app, id)
    event = event_service.delete(id)
    return Response(req, event).update

##############
# Mint Links #
##############


@app.post('/.+/mint_links')
@tracer.capture_method
def create_mint_link():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    mint_link = mint_link_service.create(body)
    return Response(req, mint_link).create


@app.get('/.+/mint_links')
@tracer.capture_method
def list_mint_links():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    mint_links = mint_link_service.list(filter, limit, skip)
    mint_links = mint_link_service.expand(mint_links, req.expand_list)
    mint_links = mint_links.get('data', [])  # type: ignore
    count = mint_link_service.count(req.filter)
    return Response(req, mint_links, count).list


@app.get('/.+/mint_links/<id>')
@tracer.capture_method
def get_mint_link(id):
    req = Request(app, id)
    mint_link = mint_link_service.retrieve_by_id(id)
    mint_link = mint_link_service.expand(mint_link, req.expand_list)
    return Response(req, mint_link).get


@app.put('/.+/mint_links/<id>')
@tracer.capture_method
def update_mint_link(id):
    req = Request(app, id)
    mint_link = mint_link_service.update(id, req.body)
    return Response(req, mint_link).update


@app.put('/.+/mint_links/<id>/archive')
@tracer.capture_method
def archive_mint_link(id):
    req = Request(app, id)
    mint_link = mint_link_service.archive(id)
    return Response(req, mint_link).update


@app.delete('/.+/mint_links/<id>')
@tracer.capture_method
def delete_mint_link(id):
    req = Request(app, id)
    mint_link = mint_link_service.delete(id)
    return Response(req, mint_link).update

#########
# Mints #
#########


@app.post('/.+/mints')
@tracer.capture_method
def create_mint():
    req = Request(app)
    body = req.body
    body['email'] = req.email
    mint = mint_service.create(body)
    return Response(req, mint).create


@app.get('/.+/mints')
@tracer.capture_method
def list_mints():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    mints = mint_service.list(filter, limit, skip)
    mints = mint_service.expand(mints, req.expand_list)
    mints = mints.get('data', [])  # type: ignore
    count = mint_service.count(req.filter)
    return Response(req, mints, count).list


@app.get('/.+/mints/<id>')
@tracer.capture_method
def get_mint(id):
    req = Request(app, id)
    mint = mint_service.retrieve_by_id(id)
    mint = mint_service.expand(mint, req.expand_list)
    return Response(req, mint).get


@app.put('/.+/mints/<id>')
@tracer.capture_method
def update_mint(id):
    req = Request(app, id)
    mint = mint_service.update(id, req.body)
    return Response(req, mint).update


@app.delete('/.+/mints/<id>')
@tracer.capture_method
def delete_mint(id):
    req = Request(app, id)
    mint = mint_service.delete(id)
    return Response(req, mint).update


@app.put('/.+/mints/<id>/fulfill')
@tracer.capture_method
def fulfill_mint(id):
    req = Request(app, id)
    mint = mint_service.fulfill(id, req.body)
    return Response(req, mint).update


#########
# Notes #
#########


@app.post('/.+/notes')
@tracer.capture_method
def create_note():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    note = note_service.create(body)
    return Response(req, note).create


@app.get('/.+/notes')
@tracer.capture_method
def list_notes():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    notes = note_service.list(filter, limit, skip)
    notes = note_service.expand(notes, req.expand_list)
    notes = notes.get('data', [])  # type: ignore
    count = note_service.count(req.filter)
    return Response(req, notes, count).list


@app.get('/.+/notes/<id>')
@tracer.capture_method
def get_note(id):
    req = Request(app, id)
    note = note_service.retrieve_by_id(id)
    note = note_service.expand(note, req.expand_list)
    return Response(req, note).get


@app.put('/.+/notes/<id>')
@tracer.capture_method
def update_note(id):
    req = Request(app, id)
    note = note_service.update(id, req.body)
    return Response(req, note).update


@app.delete('/.+/notes/<id>')
@tracer.capture_method
def delete_note(id):
    req = Request(app, id)
    note = note_service.delete(id)
    return Response(req, note).update


############
# Products #
############


@app.post('/.+/products')
@tracer.capture_method
def create_product():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    product = product_service.create(body)
    return Response(req, product).create


@app.get('/.+/products')
@tracer.capture_method
def list_products():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    products = product_service.list(filter, limit, skip)
    products = product_service.expand(products, req.expand_list)
    products = products.get('data', [])  # type: ignore
    count = product_service.count(req.filter)
    return Response(req, products, count).list


@app.get('/.+/products/<id>')
@tracer.capture_method
def get_product(id):
    req = Request(app, id)
    product = product_service.retrieve_by_id(id)
    product = product_service.expand(product, req.expand_list)
    return Response(req, product).get


@app.put('/.+/products/<id>')
@tracer.capture_method
def update_product(id):
    req = Request(app, id)
    product = product_service.update(id, req.body)
    return Response(req, product).update


@app.delete('/.+/products/<id>')
@tracer.capture_method
def delete_product(id):
    req = Request(app, id)
    product = product_service.delete(id)
    return Response(req, product).update


##########
# Search #
##########


class SearchType(Enum):
    """An enumerations of the supported search types."""

    AggregateTags = "aggregate_tags"
    CountSegmentContacts = "count_segment_contacts"
    ListSegmentContacts = "list_segment_contacts"
    MintReport = 'mint_report'
    SearchContacts = "search_contacts"
    SearchProducts = "search_products"
    UsageStats = 'usage_stats'


@app.get('/.+/search')
@tracer.capture_method
def search():
    query_params = app.current_event.query_string_parameters or {}

    # Parse request for params
    search_type = query_params.get('search_type')
    account = app.current_event.get_header_value('Versify-Account')
    query = query_params.get('query', '')
    vql = query_params.get('vql', '')
    url = app.current_event.path

    data = None
    if search_type == SearchType.AggregateTags.value:
        data = contact_service.aggregate_tags(account)
    elif search_type == SearchType.CountSegmentContacts.value:
        data = contact_service.count_segment_contacts(account, vql)
    elif search_type == SearchType.ListSegmentContacts.value:
        data = contact_service.list_segment_contacts(account, vql)
    elif search_type == SearchType.MintReport.value:
        data = mint_service.generate_report(account, vql)
    elif search_type == SearchType.SearchContacts.value:
        data = contact_service.search(account, query)
    elif search_type == SearchType.SearchProducts.value:
        data = product_service.search(account, query)
    else:
        e = f"'{search_type}' is not a valid Search Type"
        raise BadRequestError(e)

    return {
        'object': 'search',
        'url': url,
        'has_more': False,
        'data': data
    }

##############
# Signatures #
##############


@app.get('/.+/signatures/<id>')
@tracer.capture_method
def get_signature(id):
    return signature_service.exists(id)


############
# Users #
############


@app.post('/.+/users')
@tracer.capture_method
def login_user():
    req = Request(app)
    user = user_service.login(req.body)
    return Response(req, user).create


############
# Webhooks #
############


@app.post('/.+/webhooks')
@tracer.capture_method
def create_webhook():
    req = Request(app)
    body = req.body
    body['account'] = req.account
    webhook = webhook_service.create(body)
    return Response(req, webhook).create


@app.get('/.+/webhooks')
@tracer.capture_method
def list_webhooks():
    req = Request(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    webhooks = webhook_service.list(filter, limit, skip)
    webhooks = webhook_service.expand(webhooks, req.expand_list)
    webhooks = webhooks.get('data', [])  # type: ignore
    count = webhook_service.count(req.filter)
    return Response(req, webhooks, count).list


@app.get('/.+/webhooks/<id>')
@tracer.capture_method
def get_webhook(id):
    req = Request(app, id)
    webhook = webhook_service.retrieve_by_id(id)
    webhook = webhook_service.expand(webhook, req.expand_list)
    return Response(req, webhook).get


@app.put('/.+/webhooks/<id>')
@tracer.capture_method
def update_webhook(id):
    req = Request(app, id)
    webhook = webhook_service.update(id, req.body)
    return Response(req, webhook).update


@app.delete('/.+/webhooks/<id>')
@tracer.capture_method
def delete_webhook(id):
    req = Request(app, id)
    webhook = webhook_service.delete(id)
    return Response(req, webhook).update


####################
# Partner Webhooks #
####################


@app.post("/webhook/alchemy")
@tracer.capture_method
def alchemy_partner_connector():
    """Consume events from Alchemy and pubish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = 'transaction.created'
    detail = payload
    event_bus = 'partner'
    source = 'alchemy'
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@app.post("/webhook/stripe")
@tracer.capture_method
def stripe_partner_connector():
    """Consume events from Stripe and pubish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = 'event.created'
    detail = payload
    event_bus = 'partner'
    source = 'stripe'
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@app.post("/webhook/tatum")
@tracer.capture_method
def tatum_partner_connector():
    """Consume events from Tatum and pubish to the PartnerBus"""
    payload = app.current_event.json_body
    detail_type = 'transaction.created'
    detail = payload
    event_bus = 'partner'
    source = 'tatum'
    response = publish_event(detail_type, detail, event_bus, source)
    return response


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)