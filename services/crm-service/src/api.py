from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers
from versify.utilities.model import response

from .service import Versify

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


@tracer.capture_method
def sync(app):
    organization = app.current_event.get_header_value('X-Organization')
    versify = Versify(organization)
    return versify


"""
Contact Endpoints
"""


@app.get("/crm/v1/contacts")
@tracer.capture_method
def list_contacts():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters
    contacts = versify.contacts.list(query_params)
    return response('list', contacts, 'contact', '/contacts', False)


@app.post("/crm/v1/contacts")
@tracer.capture_method
def create_contact():
    versify = sync(app)
    payload = app.current_event.json_body
    contact = versify.contacts.create(payload)
    return response('create', contact)


@app.get("/crm/v1/contacts/<contact_id>")
@tracer.capture_method
def get_contact(contact_id):
    versify = sync(app)
    contact = versify.contacts.get(contact_id)
    return response('get', contact)


@app.put("/crm/v1/contacts/<contact_id>")
@tracer.capture_method
def update_contact(contact_id):
    versify = sync(app)
    payload = app.current_event.json_body
    contact = versify.contacts.update(contact_id, payload)
    return response('update', contact)


@app.delete("/crm/v1/contacts/<contact_id>")
@tracer.capture_method
def delete_contact(contact_id):
    versify = sync(app)
    versify.contacts.delete(contact_id)
    return response('delete', contact_id)


@app.put("/crm/v1/contacts/<contact_id>/actions/archive")
@tracer.capture_method
def archive_contact(contact_id):
    versify = sync(app)
    contact = versify.contacts.archive(contact_id)
    return response('update', contact)


@app.put("/crm/v1/contacts/<contact_id>/actions/unarchive")
@tracer.capture_method
def unarchive_contact(contact_id):
    versify = sync(app)
    contact = versify.contacts.unarchive(contact_id)
    return response('update', contact)


@app.get("/crm/v1/contacts/<contact_id>/notes")
@tracer.capture_method
def list_contact_notes(contact_id):
    versify = sync(app)
    notes = versify.notes.list_by_contact(contact_id)
    return response('list', notes, 'note', '/contacts/{contact_id}/notes', False)


@app.post("/crm/v1/contacts/<contact_id>/notes")
@tracer.capture_method
def create_contact_note(contact_id):
    versify = sync(app)
    payload = app.current_event.json_body
    note = versify.notes.create(contact_id, payload)
    return response('create', note)


@app.delete("/crm/v1/contacts/<contact_id>/notes/<note_id>")
@tracer.capture_method
def delete_contact_note(contact_id, note_id):
    versify = sync(app)
    versify.notes.delete(contact_id, note_id)
    return response('delete', note_id)


@app.get("/crm/v1/contacts/<contact_id>/tags")
@tracer.capture_method
def list_contact_tags(contact_id):
    versify = sync(app)
    tags = versify.tags.list_by_contact(contact_id)
    return response('list', tags, 'tag', '/contacts/{contact_id}/tags', False)


@app.post("/crm/v1/contacts/<contact_id>/tags")
@tracer.capture_method
def create_contact_tag(contact_id):
    versify = sync(app)
    payload = app.current_event.json_body
    tag = versify.tags.create(payload, contact_id)
    return response('create', tag)


"""
Tag Endpoints
"""


@app.get("/crm/v1/tags")
@tracer.capture_method
def list_tags():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters
    tags = versify.tags.list_by_org(query_params)
    return response('list', tags, 'tag', '/tags', False)


@app.post("/crm/v1/tags")
@tracer.capture_method
def create_tag():
    versify = sync(app)
    payload = app.current_event.json_body
    tag = versify.tags.create(payload)
    return response('create', tag)


"""
Backend Endpoints
"""


@app.get("/crm/v1/backend/contacts")
@tracer.capture_method
def list_contacts():
    versify = sync(app)
    query_params = app.current_event.query_string_parameters
    contacts = versify.contacts.list(query_params)
    return response('list', contacts, 'contact', '/contacts', False)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
