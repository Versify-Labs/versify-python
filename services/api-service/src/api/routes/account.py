from enum import Enum

from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths

from versify import Versify
from versify.decorators import account_required, cors_headers

from ...api.errors import BadRequestError
from ..rest import (
    AccountRequest,
    CreateResponse,
    DeleteResponse,
    GetResponse,
    ListResponse,
    UpdateResponse,
)

app = APIGatewayRestResolver(strip_prefixes=["/v1"])
logger = Logger()
tracer = Tracer()
versify = Versify()


############
# Accounts #
############


@app.get("/accounts/<id>")
@tracer.capture_method
def get_account(id):
    req = AccountRequest(app, id)
    account = versify.account_service.retrieve_by_id(id)
    return GetResponse(req, account).json


@app.put("/accounts/<id>")
@tracer.capture_method
def update_account(id):
    req = AccountRequest(app, id)
    account = versify.account_service.update(id, req.body)
    return UpdateResponse(req, account).json


@app.post("/accounts/<id>/billing")
@tracer.capture_method
def create_account_billing_session(id):
    req = AccountRequest(app, id)
    checkout = versify.account_service.create_billing_session(id)
    return CreateResponse(req, checkout).json


@app.get("/accounts/<id>/billing/summary")
@tracer.capture_method
def get_account_billing_summary(id):
    req = AccountRequest(app, id)
    summary = versify.account_service.get_billing_summary(id)
    return GetResponse(req, summary).json


@app.post("/accounts/<id>/checkout")
@tracer.capture_method
def create_account_checkout_session(id):
    req = AccountRequest(app, id)
    checkout = versify.account_service.create_checkout_session(id)
    return CreateResponse(req, checkout).json


@app.get("/accounts/<id>/invoices")
@tracer.capture_method
def list_account_invoices(id):
    req = AccountRequest(app, id)
    account_id = req.account or id
    invoices = versify.account_service.list_invoices(account_id)
    return GetResponse(req, invoices).json


@app.post("/accounts/<id>/members")
@tracer.capture_method
def create_account_member(id):
    req = AccountRequest(app, id)
    body = req.body
    body["account"] = req.account
    member = versify.account_service.create_member(id, body)
    return CreateResponse(req, member).json


@app.get("/accounts/<id>/members")
@tracer.capture_method
def list_account_members(id):
    req = AccountRequest(app, id)
    account_id = req.account or id
    members = versify.account_service.list_members(account_id)
    return GetResponse(req, members).json


@app.get("/accounts/<id>/metrics")
@tracer.capture_method
def list_account_metrics(id):
    req = AccountRequest(app, id)
    objects = req.filter.get("objects", "")
    account = versify.account_service.list_metrics(id, objects)
    return GetResponse(req, account).json


@app.get("/accounts/<id>/subscriptions")
@tracer.capture_method
def list_account_subscriptions(id):
    req = AccountRequest(app, id)
    account_id = req.account or id
    subscriptions = versify.account_service.list_subscriptions(account_id)
    return GetResponse(req, subscriptions).json


@app.post("/accounts/<id>/tokens")
@tracer.capture_method
def create_account_token(id):
    req = AccountRequest(app, id)
    account_id = req.account
    token = versify.account_service.create_token(account_id)  # type: ignore
    return GetResponse(req, token).json  # type: ignore


############
# Airdrops #
############


@app.post("/airdrops")
@tracer.capture_method
def create_airdrop():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    airdrop = versify.airdrop_service.create(body)
    return CreateResponse(req, airdrop).json


@app.get("/airdrops")
@tracer.capture_method
def list_airdrops():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.airdrop_service.count(req.filter)
    airdrops = versify.airdrop_service.list(filter, limit, skip)
    airdrops = versify.airdrop_service.expand(airdrops, req.expand_list)
    airdrops = airdrops.get("data", [])  # type: ignore
    return ListResponse(req, airdrops, count).json


@app.get("/airdrops/<id>")
@tracer.capture_method
def get_airdrop(id):
    req = AccountRequest(app, id)
    airdrop = versify.airdrop_service.retrieve_by_id(id)
    airdrop = versify.airdrop_service.expand(airdrop, req.expand_list)
    return GetResponse(req, airdrop).json


@app.put("/airdrops/<id>")
@tracer.capture_method
def update_airdrop(id):
    req = AccountRequest(app, id)
    airdrop = versify.airdrop_service.update(id, req.body)
    return UpdateResponse(req, airdrop).json


@app.put("/airdrops/<id>/send")
@tracer.capture_method
def send_airdrop(id):
    req = AccountRequest(app, id)
    airdrop = versify.airdrop_service.send(id)
    return UpdateResponse(req, airdrop).json


##########
# Claims #
##########


@app.post("/claims")
@tracer.capture_method
def create_claim():
    req = AccountRequest(app)
    body = req.body
    claim = versify.claim_service.create(body)
    return CreateResponse(req, claim).json


@app.get("/claims")
@tracer.capture_method
def list_claims():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.claim_service.count(req.filter)
    claims = versify.claim_service.list(filter, limit, skip)
    claims = versify.claim_service.expand(claims, req.expand_list)
    claims = claims.get("data", [])  # type: ignore
    return ListResponse(req, claims, count).json


@app.get("/claims/<id>")
@tracer.capture_method
def get_claim(id):
    req = AccountRequest(app, id)
    claim = versify.claim_service.retrieve_by_id(id)
    claim = versify.claim_service.expand(claim, req.expand_list)
    return GetResponse(req, claim).json


###############
# Collections #
###############


@app.post("/collections")
@tracer.capture_method
def create_collection():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    collection = versify.collection_service.create(body)
    return CreateResponse(req, collection).json


@app.get("/collections")
@tracer.capture_method
def list_collections():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.collection_service.count(req.filter)
    collections = versify.collection_service.list(filter, limit, skip)
    collections = versify.collection_service.expand(collections, req.expand_list)
    collections = collections.get("data", [])  # type: ignore
    return ListResponse(req, collections, count).json


@app.get("/collections/<id>")
@tracer.capture_method
def get_collection(id):
    req = AccountRequest(app, id)
    collection = versify.collection_service.retrieve(id)
    collection = versify.collection_service.expand(collection, req.expand_list)
    return GetResponse(req, collection).json


@app.put("/collections/<id>")
@tracer.capture_method
def update_collection(id):
    req = AccountRequest(app, id)
    collection = versify.collection_service.update(id, req.body)
    return UpdateResponse(req, collection).json


############
# Contacts #
############


@app.post("/contacts")
@tracer.capture_method
def create_contact():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    contact = versify.contact_service.create(body)
    return CreateResponse(req, contact).json


@app.get("/contacts")
@tracer.capture_method
def list_contacts():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.contact_service.count(req.filter)
    contacts = versify.contact_service.list(filter, limit, skip)
    contacts = versify.contact_service.expand(contacts, req.expand_list)
    contacts = contacts.get("data", [])  # type: ignore
    return ListResponse(req, contacts, count).json


@app.put("/contacts")
@tracer.capture_method
def update_contacts():
    req = AccountRequest(app)
    ids = req.body.get("ids", [])
    update_body = req.body.get("body", {})
    modified = versify.contact_service.bulk_update(ids, update_body)
    return {"modified": modified}


@app.get("/contacts/<id>")
@tracer.capture_method
def get_contact(id):
    req = AccountRequest(app, id)
    contact = versify.contact_service.get(id)
    contact = versify.contact_service.expand(contact, req.expand_list)
    return GetResponse(req, contact).json  # type: ignore


@app.put("/contacts/<id>")
@tracer.capture_method
def update_contact(id):
    req = AccountRequest(app, id)
    contact = versify.contact_service.update(id, req.body)
    return UpdateResponse(req, contact).json


@app.post("/contacts/<id>/notes")
@tracer.capture_method
def create_contact_note(id):
    req = AccountRequest(app, id)
    body = req.body
    if body.get("user") is None:
        body["user"] = {"id": req.user or "system", "email": req.email}
    note = versify.contact_service.create_note(id, body)
    return CreateResponse(req, note).json  # type: ignore


@app.delete("/contacts/<id>/notes/<note_id>")
@tracer.capture_method
def delete_contact_note(id, note_id):
    req = AccountRequest(app, id)
    versify.contact_service.delete_note(id, note_id)
    return DeleteResponse(req).json


##########
# Events #
##########


@app.post("/events")
@tracer.capture_method
def create_event():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    event = versify.event_service.create(body)
    return CreateResponse(req, event).json


@app.get("/events")
@tracer.capture_method
def list_events():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.event_service.count(req.filter)
    events = versify.event_service.list(filter, limit, skip)
    events = versify.event_service.expand(events, req.expand_list)
    events = events.get("data", [])  # type: ignore
    return ListResponse(req, events, count).json


@app.get("/events/<id>")
@tracer.capture_method
def get_event(id):
    req = AccountRequest(app, id)
    event = versify.event_service.get(id)
    event = versify.event_service.expand(event, req.expand_list)
    return GetResponse(req, event).json  # type: ignore


############
# Journeys #
############


@app.post("/journeys")
@tracer.capture_method
def create_journey():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    journey = versify.journey_service.create(body)
    return CreateResponse(req, journey).json


@app.get("/journeys")
@tracer.capture_method
def list_journeys():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.journey_service.count(req.filter)
    journeys = versify.journey_service.list(filter, limit, skip)
    journeys = versify.journey_service.expand(journeys, req.expand_list)
    journeys = journeys.get("data", [])  # type: ignore
    return ListResponse(req, journeys, count).json


@app.get("/journeys/<id>")
@tracer.capture_method
def get_journey(id):
    req = AccountRequest(app, id)
    journey = versify.journey_service.get(id)
    journey = versify.journey_service.expand(journey, req.expand_list)
    return GetResponse(req, journey).json


@app.put("/journeys/<id>")
@tracer.capture_method
def update_journey(id):
    req = AccountRequest(app, id)
    journey = versify.journey_service.update(id, req.body)
    return UpdateResponse(req, journey).json


@app.put("/journeys/<id>/duplicate")
@tracer.capture_method
def duplicate_journey(id):
    req = AccountRequest(app, id)
    journey = versify.journey_service.duplicate(id)
    return UpdateResponse(req, journey).json


@app.delete("/journeys/<id>")
@tracer.capture_method
def delete_journey(id):
    req = AccountRequest(app, id)
    versify.journey_service.delete(id)
    return DeleteResponse(req).json


@app.get("/journeys/<id>/runs")
@tracer.capture_method
def list_journey_runs(id):
    req = AccountRequest(app)
    filter = req.filter
    filter["journey"] = id
    limit = req.limit
    skip = req.skip
    count = versify.journey_run_service.count(req.filter)
    runs = versify.journey_run_service.list(filter, limit, skip)
    runs = versify.journey_run_service.expand(runs, req.expand_list)
    runs = runs.get("data", [])  # type: ignore
    return ListResponse(req, runs, count).json


############
# Messages #
############


@app.post("/messages")
@tracer.capture_method
def create_message():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    message = versify.message_service.create(body)
    return CreateResponse(req, message).json


@app.get("/messages")
@tracer.capture_method
def list_messages():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.message_service.count(req.filter)
    messages = versify.message_service.list(filter, limit, skip)
    messages = versify.message_service.expand(messages, req.expand_list)
    messages = messages.get("data", [])  # type: ignore
    return ListResponse(req, messages, count).json


@app.get("/messages/<id>")
@tracer.capture_method
def get_message(id):
    req = AccountRequest(app, id)
    message = versify.message_service.get(id)
    message = versify.message_service.expand(message, req.expand_list)
    return GetResponse(req, message).json


##############
# Mint Links #
##############


@app.post("/mint_links")
@tracer.capture_method
def create_mint_link():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    mint_link = versify.mint_link_service.create(body)
    return CreateResponse(req, mint_link).json


@app.get("/mint_links")
@tracer.capture_method
def list_mint_links():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.mint_link_service.count(req.filter)
    mint_links = versify.mint_link_service.list(filter, limit, skip)
    mint_links = versify.mint_link_service.expand(mint_links, req.expand_list)
    mint_links = mint_links.get("data", [])  # type: ignore
    return ListResponse(req, mint_links, count).json


@app.get("/mint_links/<id>")
@tracer.capture_method
def get_mint_link(id):
    req = AccountRequest(app, id)
    mint_link = versify.mint_link_service.retrieve_by_id(id)
    mint_link = versify.mint_link_service.expand(mint_link, req.expand_list)
    return GetResponse(req, mint_link).json


@app.put("/mint_links/<id>")
@tracer.capture_method
def update_mint_link(id):
    req = AccountRequest(app, id)
    mint_link = versify.mint_link_service.update(id, req.body)
    return UpdateResponse(req, mint_link).json


@app.put("/mint_links/<id>/archive")
@tracer.capture_method
def archive_mint_link(id):
    req = AccountRequest(app, id)
    mint_link = versify.mint_link_service.archive(id)
    return UpdateResponse(req, mint_link).json


#########
# Mints #
#########


@app.post("/mints")
@tracer.capture_method
def create_mint():
    req = AccountRequest(app)
    body = req.body
    mint = versify.mint_service.create(body)
    return CreateResponse(req, mint).json


@app.get("/mints")
@tracer.capture_method
def list_mints():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.mint_service.count(req.filter)
    mints = versify.mint_service.list(filter, limit, skip)
    mints = versify.mint_service.expand(mints, req.expand_list)
    mints = mints.get("data", [])  # type: ignore
    return ListResponse(req, mints, count).json


@app.get("/mints/<id>")
@tracer.capture_method
def get_mint(id):
    req = AccountRequest(app, id)
    mint = versify.mint_service.retrieve_by_id(id)
    mint = versify.mint_service.expand(mint, req.expand_list)
    return GetResponse(req, mint).json


############
# Products #
############


@app.post("/products")
@tracer.capture_method
def create_product():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    product = versify.product_service.create(body)
    return CreateResponse(req, product).json


@app.get("/products")
@tracer.capture_method
def list_products():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.product_service.count(req.filter)
    products = versify.product_service.list(filter, limit, skip)
    products = versify.product_service.expand(products, req.expand_list)
    products = products.get("data", [])  # type: ignore
    return ListResponse(req, products, count).json


@app.get("/products/<id>")
@tracer.capture_method
def get_product(id):
    req = AccountRequest(app, id)
    product = versify.product_service.retrieve_by_id(id)
    product = versify.product_service.expand(product, req.expand_list)
    return GetResponse(req, product).json


@app.put("/products/<id>")
@tracer.capture_method
def update_product(id):
    req = AccountRequest(app, id)
    product = versify.product_service.update(id, req.body)
    return UpdateResponse(req, product).json


###########
# Rewards #
###########


@app.post("/rewards")
@tracer.capture_method
def create_reward():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    reward = versify.reward_service.create(body)
    return CreateResponse(req, reward).json


@app.get("/rewards")
@tracer.capture_method
def list_rewards():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.reward_service.count(req.filter)
    rewards = versify.reward_service.list(filter, limit, skip)
    rewards = versify.reward_service.expand(rewards, req.expand_list)
    rewards = rewards.get("data", [])  # type: ignore
    return ListResponse(req, rewards, count).json


@app.get("/rewards/<id>")
@tracer.capture_method
def get_reward(id):
    req = AccountRequest(app, id)
    reward = versify.reward_service.get(id)
    reward = versify.reward_service.expand(reward, req.expand_list)
    return GetResponse(req, reward).json


@app.put("/rewards/<id>")
@tracer.capture_method
def update_reward(id):
    req = AccountRequest(app, id)
    reward = versify.reward_service.update(id, req.body)
    return UpdateResponse(req, reward).json


@app.post("/rewards/<id>/redemptions")
@tracer.capture_method
def create_reward_redemption(id):
    req = AccountRequest(app, id)
    body = req.body
    body["reward"] = id
    redemption = versify.redemption_service.create(body)
    return CreateResponse(req, redemption).json


@app.get("/rewards/<id>/redemptions")
@tracer.capture_method
def list_reward_redemptions(id):
    req = AccountRequest(app)
    filter = req.filter
    filter["reward"] = id
    limit = req.limit
    skip = req.skip
    count = versify.redemption_service.count(req.filter)
    runs = versify.redemption_service.list(filter, limit, skip)
    runs = versify.redemption_service.expand(runs, req.expand_list)
    runs = runs.get("data", [])  # type: ignore
    return ListResponse(req, runs, count).json


##########
# Search #
##########


class SearchType(Enum):
    """An enumerations of the supported search types."""

    AggregateTags = "aggregate_tags"
    CountSegmentContacts = "count_segment_contacts"
    ListSegmentContacts = "list_segment_contacts"
    MintReport = "mint_report"
    SearchAirdrops = "search_airdrops"
    SearchContacts = "search_contacts"
    SearchProducts = "search_products"
    UsageStats = "usage_stats"


@app.get("/search")
@tracer.capture_method
def search():
    query_params = app.current_event.query_string_parameters or {}

    # Parse request for params
    account = app.current_event.get_header_value("Versify-Account")
    search_type = query_params.get("search_type")
    query = query_params.get("query", "")
    vql = query_params.get("vql", "")
    url = app.current_event.path

    data = None
    if search_type == SearchType.AggregateTags.value:
        data = versify.contact_service.aggregate_tags(account)
    elif search_type == SearchType.CountSegmentContacts.value:
        data = versify.contact_service.count_segment_contacts(account, vql)
    elif search_type == SearchType.ListSegmentContacts.value:
        data = versify.contact_service.list_segment_contacts(account, vql)
    elif search_type == SearchType.MintReport.value:
        data = versify.mint_service.generate_report(account, vql)
    elif search_type == SearchType.SearchAirdrops.value:
        data = versify.airdrop_service.search(account, query)
    elif search_type == SearchType.SearchContacts.value:
        data = versify.contact_service.search(account, query)
    elif search_type == SearchType.SearchProducts.value:
        data = versify.product_service.search(account, query)
    else:
        e = f"'{search_type}' is not a valid Search Type"
        raise BadRequestError(e)

    return {"object": "search", "url": url, "has_more": False, "data": data}


############
# Webhooks #
############


@app.post("/webhooks")
@tracer.capture_method
def create_webhook():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    webhook = versify.webhook_service.create(body)
    return CreateResponse(req, webhook).json


@app.get("/webhooks")
@tracer.capture_method
def list_webhooks():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    webhooks = versify.webhook_service.list(filter, limit, skip)
    webhooks = versify.webhook_service.expand(webhooks, req.expand_list)
    webhooks = webhooks.get("data", [])  # type: ignore
    count = versify.webhook_service.count(req.filter)
    return ListResponse(req, webhooks, count).json


@app.get("/webhooks/<id>")
@tracer.capture_method
def get_webhook(id):
    req = AccountRequest(app, id)
    webhook = versify.webhook_service.get(id)
    webhook = versify.webhook_service.expand(webhook, req.expand_list)
    return GetResponse(req, webhook).json


@app.put("/webhooks/<id>")
@tracer.capture_method
def update_webhook(id):
    req = AccountRequest(app, id)
    webhook = versify.webhook_service.update(id, req.body)
    return UpdateResponse(req, webhook).json


@app.delete("/webhooks/<id>")
@tracer.capture_method
def delete_webhook(id):
    req = AccountRequest(app, id)
    versify.webhook_service.delete(id)
    return DeleteResponse(req).json


##################
# Webhook Events #
##################


@app.post("/webhook_events")
@tracer.capture_method
def create_webhook_event():
    req = AccountRequest(app)
    body = req.body
    body["account"] = req.account
    event = versify.webhook_event_service.create(body)
    return CreateResponse(req, event).json


@app.get("/webhook_events")
@tracer.capture_method
def list_webhook_events():
    req = AccountRequest(app)
    filter = req.filter
    limit = req.limit
    skip = req.skip
    count = versify.webhook_event_service.count(filter)
    events = versify.webhook_event_service.list(filter, limit, skip)
    events = versify.webhook_event_service.expand(events, req.expand_list)
    events = events.get("data", [])  # type: ignore
    return ListResponse(req, events, count).json


@app.get("/webhook_events/<id>")
@tracer.capture_method
def get_webhook_event(id):
    req = AccountRequest(app, id)
    event = versify.webhook_event_service.get(id)
    event = versify.webhook_event_service.expand(event, req.expand_list)
    return GetResponse(req, event).json


@account_required
@cors_headers
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
