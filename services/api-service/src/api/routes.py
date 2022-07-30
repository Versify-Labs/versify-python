from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from .resources import Signature, Versify
from .rest import Request, Response
from .search import Search

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
versify = Versify()


############
# Accounts #
############


@app.post('/.+/accounts')
@tracer.capture_method
def create_account():
    req = Request(app)
    data = versify.account.create(**req.create)
    return Response(req, data).create


@app.get('/.+/accounts/<id>')
@tracer.capture_method
def get_account(id):
    req = Request(app, id)
    data = versify.account.get(**req.get)
    return Response(req, data).get


@app.put('/.+/accounts/<id>')
@tracer.capture_method
def update_account(id):
    req = Request(app, id)
    data = versify.account.update(**req.update)
    return Response(req, data).update


@app.post('/.+/accounts/<id>/members')
@tracer.capture_method
def create_account_member(id):
    req = Request(app, id)
    data = versify.account.create_member(**req.create)
    return Response(req, data).create


@app.post('/.+/accounts/<id>/subscriptions')
@tracer.capture_method
def create_account_subscription(id):
    req = Request(app, id)
    data = versify.account.create_subscription(**req.create)
    return Response(req, data).create


@app.put('/.+/accounts/<id>/subscriptions/<sid>')
@tracer.capture_method
def update_account_subscription(id, sid):
    req = Request(app, id)
    data = versify.account.update_subscription(sid, req.body)
    return Response(req, data).update


############
# Airdrops #
############


@app.get('/.+/airdrops')
@tracer.capture_method
def list_airdrops():
    req = Request(app)
    data = versify.airdrop.list(**req.list)
    count = versify.airdrop.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/airdrops')
@tracer.capture_method
def create_airdrop():
    req = Request(app)
    data = versify.airdrop.create(**req.create)
    return Response(req, data).create


@app.get('/.+/airdrops/<id>')
@tracer.capture_method
def get_airdrop(id):
    req = Request(app, id)
    data = versify.airdrop.get(**req.get)
    return Response(req, data).get


@app.put('/.+/airdrops/<id>')
@tracer.capture_method
def update_airdrop(id):
    req = Request(app, id)
    data = versify.airdrop.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/airdrops/<id>')
@tracer.capture_method
def delete_airdrop(id):
    req = Request(app, id)
    versify.airdrop.delete(**req.delete)
    return Response(req).delete


@app.put('/.+/airdrops/<id>/send')
@tracer.capture_method
def send_airdrop(id):
    req = Request(app, id)
    req.body = {'status': 'sending'}
    data = versify.airdrop.update(**req.update)
    return Response(req, data).update

###############
# Collections #
###############


@app.get('/.+/collections')
@tracer.capture_method
def list_collections():
    req = Request(app)
    data = versify.collection.list(**req.list)
    count = versify.collection.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/collections')
@tracer.capture_method
def create_collection():
    req = Request(app)
    data = versify.collection.create(**req.create)
    return Response(req, data).create


@app.get('/.+/collections/<id>')
@tracer.capture_method
def get_collection(id):
    req = Request(app, id)
    data = versify.collection.get(**req.get)
    return Response(req, data).get


@app.put('/.+/collections/<id>')
@tracer.capture_method
def update_collection(id):
    req = Request(app, id)
    data = versify.collection.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/collections/<id>')
@tracer.capture_method
def delete_collection(id):
    req = Request(app, id)
    versify.collection.delete(**req.delete)
    return Response(req).delete


############
# Contacts #
############

@app.get('/.+/contacts')
@tracer.capture_method
def list_contacts():
    req = Request(app)
    data = versify.contact.list(**req.list)
    count = versify.contact.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/contacts')
@tracer.capture_method
def create_contact():
    req = Request(app)
    data = versify.contact.create(**req.create)
    return Response(req, data).create


@app.get('/.+/contacts/<id>')
@tracer.capture_method
def get_contact(id):
    req = Request(app, id)
    data = versify.contact.get(**req.get)
    return Response(req, data).get


@app.put('/.+/contacts/<id>')
@tracer.capture_method
def update_contact(id):
    req = Request(app, id)
    data = versify.contact.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/contacts/<id>')
@tracer.capture_method
def delete_contact(id):
    req = Request(app, id)
    versify.contact.delete(**req.delete)
    return Response(req).delete


##########
# Events #
##########


@app.get('/.+/events')
@tracer.capture_method
def list_events():
    req = Request(app)
    data = versify.event.list(**req.list)
    count = versify.event.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/events')
@tracer.capture_method
def create_event():
    req = Request(app)
    data = versify.event.create(**req.create)
    return Response(req, data).create


@app.get('/.+/events/<id>')
@tracer.capture_method
def get_event(id):
    req = Request(app, id)
    data = versify.event.get(**req.get)
    return Response(req, data).get


@app.put('/.+/events/<id>')
@tracer.capture_method
def update_event(id):
    req = Request(app, id)
    data = versify.event.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/events/<id>')
@tracer.capture_method
def delete_event(id):
    req = Request(app, id)
    versify.event.delete(**req.delete)
    return Response(req).delete


##############
# Mint Links #
##############

@app.get('/.+/mint_links')
@tracer.capture_method
def list_mint_links():
    req = Request(app)
    data = versify.mint_link.list(**req.list)
    count = versify.mint_link.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/mint_links')
@tracer.capture_method
def create_mint_link():
    req = Request(app)
    data = versify.mint_link.create(**req.create)
    return Response(req, data).create


@app.get('/.+/mint_links/<id>')
@tracer.capture_method
def get_mint_link(id):
    req = Request(app, id)
    data = versify.mint_link.get(**req.get)
    return Response(req, data).get


@app.put('/.+/mint_links/<id>')
@tracer.capture_method
def update_mint_link(id):
    req = Request(app, id)
    data = versify.mint_link.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/mint_links/<id>')
@tracer.capture_method
def delete_mint_link(id):
    req = Request(app, id)
    versify.mint_link.delete(**req.delete)
    return Response(req).delete


#########
# Mints #
#########
@app.get('/.+/mints')
@tracer.capture_method
def list_mints():
    req = Request(app)
    data = versify.mint.list(**req.list)
    count = versify.mint.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/mints')
@tracer.capture_method
def create_mint():
    req = Request(app)
    data = versify.mint.create(**req.create)
    return Response(req, data).create


@app.get('/.+/mints/<id>')
@tracer.capture_method
def get_mint(id):
    req = Request(app, id)
    data = versify.mint.get(**req.get)
    return Response(req, data).get


@app.put('/.+/mints/<id>')
@tracer.capture_method
def update_mint(id):
    req = Request(app, id)
    data = versify.mint.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/mints/<id>')
@tracer.capture_method
def delete_mint(id):
    req = Request(app, id)
    versify.mint.delete(**req.delete)
    return Response(req).delete


@app.put('/.+/mints/<id>/fulfill')
@tracer.capture_method
def fulfill_mint(id):
    req = Request(app, id)
    data = versify.mint.fulfill(**req.update)
    return Response(req, data).update

#########
# Notes #
#########


@app.get('/.+/notes')
@tracer.capture_method
def list_notes():
    req = Request(app)
    data = versify.note.list(**req.list)
    count = versify.note.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/notes')
@tracer.capture_method
def create_note():
    req = Request(app)
    data = versify.note.create(**req.create)
    return Response(req, data).create


@app.get('/.+/notes/<id>')
@tracer.capture_method
def get_note(id):
    req = Request(app, id)
    data = versify.note.get(**req.get)
    return Response(req, data).get


@app.put('/.+/notes/<id>')
@tracer.capture_method
def update_note(id):
    req = Request(app, id)
    data = versify.note.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/notes/<id>')
@tracer.capture_method
def delete_note(id):
    req = Request(app, id)
    versify.note.delete(**req.delete)
    return Response(req).delete


############
# Products #
############

@app.get('/.+/products')
@tracer.capture_method
def list_products():
    req = Request(app)
    data = versify.product.list(**req.list)
    count = versify.product.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/products')
@tracer.capture_method
def create_product():
    req = Request(app)
    data = versify.product.create(**req.create)
    return Response(req, data).create


@app.get('/.+/products/<id>')
@tracer.capture_method
def get_product(id):
    req = Request(app, id)
    data = versify.product.get(**req.get)
    return Response(req, data).get


@app.put('/.+/products/<id>')
@tracer.capture_method
def update_product(id):
    req = Request(app, id)
    data = versify.product.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/products/<id>')
@tracer.capture_method
def delete_product(id):
    req = Request(app, id)
    versify.product.delete(**req.delete)
    return Response(req).delete


##########
# Search #
##########


@app.get('/.+/search')
@tracer.capture_method
def search():
    return Search(app).run()


##############
# Signatures #
##############


@app.get('/.+/signatures/<id>')
@tracer.capture_method
def get_signature(id):
    return Signature().exists(id)

############
# Users #
############


@app.post('/.+/users')
@tracer.capture_method
def create_user():
    req = Request(app)
    data = versify.user.create(**req.create)
    return Response(req, data).create


############
# Webhooks #
############


@app.get('/.+/webhooks')
@tracer.capture_method
def list_webhooks():
    req = Request(app)
    data = versify.webhook.list(**req.list)
    count = versify.webhook.count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/webhooks')
@tracer.capture_method
def create_webhook():
    req = Request(app)
    data = versify.webhook.create(**req.create)
    return Response(req, data).create


@app.get('/.+/webhooks/<id>')
@tracer.capture_method
def get_webhook(id):
    req = Request(app, id)
    data = versify.webhook.get(**req.get)
    return Response(req, data).get


@app.put('/.+/webhooks/<id>')
@tracer.capture_method
def update_webhook(id):
    req = Request(app, id)
    data = versify.webhook.update(**req.update)
    return Response(req, data).update


@app.delete('/.+/webhooks/<id>')
@tracer.capture_method
def delete_webhook(id):
    req = Request(app, id)
    versify.webhook.delete(**req.delete)
    return Response(req).delete


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
