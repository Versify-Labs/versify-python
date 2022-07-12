from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from .resources import (Account, Airdrop, Collection, Contact, Event, Mint,
                        MintLink, Note, Product, Signature, Webhook)
from .rest import Request, Response
from .search import Search

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()

############
# Accounts #
############


@app.get('/.+/accounts')
@tracer.capture_method
def list_accounts():
    req = Request(app)
    data = Account().list(**req.list)
    count = Account().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/accounts')
@tracer.capture_method
def create_account():
    req = Request(app)
    data = Account().create(**req.create)
    return Response(req, data).create


@app.get('/.+/accounts/<id>')
@tracer.capture_method
def get_account(id):
    req = Request(app, id)
    data = Account().get(**req.get)
    return Response(req, data).get


@app.put('/.+/accounts/<id>')
@tracer.capture_method
def update_account(id):
    req = Request(app, id)
    data = Account().update(**req.update)
    return Response(req, data).update


############
# Airdrops #
############


@app.get('/.+/airdrops')
@tracer.capture_method
def list_airdrops():
    req = Request(app)
    data = Airdrop().list(**req.list)
    count = Airdrop().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/airdrops')
@tracer.capture_method
def create_airdrop():
    req = Request(app)
    data = Airdrop().create(**req.create)
    return Response(req, data).create


@app.get('/.+/airdrops/<id>')
@tracer.capture_method
def get_airdrop(id):
    req = Request(app, id)
    data = Airdrop().get(**req.get)
    return Response(req, data).get


@app.put('/.+/airdrops/<id>')
@tracer.capture_method
def update_airdrop(id):
    req = Request(app, id)
    data = Airdrop().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/airdrops/<id>')
@tracer.capture_method
def delete_airdrop(id):
    req = Request(app, id)
    Airdrop().delete(**req.delete)
    return Response(req).delete


@app.put('/.+/airdrops/<id>/send')
@tracer.capture_method
def send_airdrop(id):
    req = Request(app, id)
    req.body = {'status': 'sending'}
    data = Airdrop().update(**req.update)
    return Response(req, data).update

###############
# Collections #
###############


@app.get('/.+/collections')
@tracer.capture_method
def list_collections():
    req = Request(app)
    data = Collection().list(**req.list)
    count = Collection().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/collections')
@tracer.capture_method
def create_collection():
    req = Request(app)
    data = Collection().create(**req.create)
    return Response(req, data).create


@app.get('/.+/collections/<id>')
@tracer.capture_method
def get_collection(id):
    req = Request(app, id)
    data = Collection().get(**req.get)
    return Response(req, data).get


@app.put('/.+/collections/<id>')
@tracer.capture_method
def update_collection(id):
    req = Request(app, id)
    data = Collection().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/collections/<id>')
@tracer.capture_method
def delete_collection(id):
    req = Request(app, id)
    Collection().delete(**req.delete)
    return Response(req).delete


############
# Contacts #
############

@app.get('/.+/contacts')
@tracer.capture_method
def list_contacts():
    req = Request(app)
    data = Contact().list(**req.list)
    count = Contact().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/contacts')
@tracer.capture_method
def create_contact():
    req = Request(app)
    data = Contact().create(**req.create)
    return Response(req, data).create


@app.get('/.+/contacts/<id>')
@tracer.capture_method
def get_contact(id):
    req = Request(app, id)
    data = Contact().get(**req.get)
    return Response(req, data).get


@app.put('/.+/contacts/<id>')
@tracer.capture_method
def update_contact(id):
    req = Request(app, id)
    data = Contact().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/contacts/<id>')
@tracer.capture_method
def delete_contact(id):
    req = Request(app, id)
    Contact().delete(**req.delete)
    return Response(req).delete


##########
# Events #
##########


@app.get('/.+/events')
@tracer.capture_method
def list_events():
    req = Request(app)
    data = Event().list(**req.list)
    count = Event().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/events')
@tracer.capture_method
def create_event():
    req = Request(app)
    data = Event().create(**req.create)
    return Response(req, data).create


@app.get('/.+/events/<id>')
@tracer.capture_method
def get_event(id):
    req = Request(app, id)
    data = Event().get(**req.get)
    return Response(req, data).get


@app.put('/.+/events/<id>')
@tracer.capture_method
def update_event(id):
    req = Request(app, id)
    data = Event().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/events/<id>')
@tracer.capture_method
def delete_event(id):
    req = Request(app, id)
    Event().delete(**req.delete)
    return Response(req).delete


##############
# Mint Links #
##############

@app.get('/.+/mint_links')
@tracer.capture_method
def list_mint_links():
    req = Request(app)
    data = MintLink().list(**req.list)
    count = MintLink().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/mint_links')
@tracer.capture_method
def create_mint_link():
    req = Request(app)
    data = MintLink().create(**req.create)
    return Response(req, data).create


@app.get('/.+/mint_links/<id>')
@tracer.capture_method
def get_mint_link(id):
    req = Request(app, id)
    data = MintLink().get(**req.get)
    return Response(req, data).get


@app.put('/.+/mint_links/<id>')
@tracer.capture_method
def update_mint_link(id):
    req = Request(app, id)
    data = MintLink().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/mint_links/<id>')
@tracer.capture_method
def delete_mint_link(id):
    req = Request(app, id)
    MintLink().delete(**req.delete)
    return Response(req).delete


#########
# Mints #
#########
@app.get('/.+/mints')
@tracer.capture_method
def list_mints():
    req = Request(app)
    data = Mint().list(**req.list)
    count = Mint().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/mints')
@tracer.capture_method
def create_mint():
    req = Request(app)
    data = Mint().create(**req.create)
    return Response(req, data).create


@app.get('/.+/mints/<id>')
@tracer.capture_method
def get_mint(id):
    req = Request(app, id)
    data = Mint().get(**req.get)
    return Response(req, data).get


@app.put('/.+/mints/<id>')
@tracer.capture_method
def update_mint(id):
    req = Request(app, id)
    data = Mint().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/mints/<id>')
@tracer.capture_method
def delete_mint(id):
    req = Request(app, id)
    Mint().delete(**req.delete)
    return Response(req).delete


@app.put('/.+/mints/<id>/fulfill')
@tracer.capture_method
def fulfill_mint(id):
    req = Request(app, id)
    req.body['status'] = 'fulfilled'
    return Mint().update(**req.update)

#########
# Notes #
#########


@app.get('/.+/notes')
@tracer.capture_method
def list_notes():
    req = Request(app)
    data = Note().list(**req.list)
    count = Note().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/notes')
@tracer.capture_method
def create_note():
    req = Request(app)
    data = Note().create(**req.create)
    return Response(req, data).create


@app.get('/.+/notes/<id>')
@tracer.capture_method
def get_note(id):
    req = Request(app, id)
    data = Note().get(**req.get)
    return Response(req, data).get


@app.put('/.+/notes/<id>')
@tracer.capture_method
def update_note(id):
    req = Request(app, id)
    data = Note().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/notes/<id>')
@tracer.capture_method
def delete_note(id):
    req = Request(app, id)
    Note().delete(**req.delete)
    return Response(req).delete


############
# Products #
############

@app.get('/.+/products')
@tracer.capture_method
def list_products():
    req = Request(app)
    data = Product().list(**req.list)
    count = Product().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/products')
@tracer.capture_method
def create_product():
    req = Request(app)
    data = Product().create(**req.create)
    return Response(req, data).create


@app.get('/.+/products/<id>')
@tracer.capture_method
def get_product(id):
    req = Request(app, id)
    data = Product().get(**req.get)
    return Response(req, data).get


@app.put('/.+/products/<id>')
@tracer.capture_method
def update_product(id):
    req = Request(app, id)
    data = Product().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/products/<id>')
@tracer.capture_method
def delete_product(id):
    req = Request(app, id)
    Product().delete(**req.delete)
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
# Webhooks #
############

@app.get('/.+/webhooks')
@tracer.capture_method
def list_webhooks():
    req = Request(app)
    data = Webhook().list(**req.list)
    count = Webhook().count(**req.count)
    return Response(req, data, count).list


@app.post('/.+/webhooks')
@tracer.capture_method
def create_webhook():
    req = Request(app)
    data = Webhook().create(**req.create)
    return Response(req, data).create


@app.get('/.+/webhooks/<id>')
@tracer.capture_method
def get_webhook(id):
    req = Request(app, id)
    data = Webhook().get(**req.get)
    return Response(req, data).get


@app.put('/.+/webhooks/<id>')
@tracer.capture_method
def update_webhook(id):
    req = Request(app, id)
    data = Webhook().update(**req.update)
    return Response(req, data).update


@app.delete('/.+/webhooks/<id>')
@tracer.capture_method
def delete_webhook(id):
    req = Request(app, id)
    Webhook().delete(**req.delete)
    return Response(req).delete


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
