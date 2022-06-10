import secrets

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from .auth0 import init_auth0

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()
auth0 = init_auth0()


@app.get("/auth/v1/tests/1")
@tracer.capture_method
def test1():
    return 'Success from test 1'


@app.get("/auth/v1/tests/2")
@tracer.capture_method
def test2():
    return 'Success from test 2'


@app.get("/auth/v1/ping")
@tracer.capture_method
def ping():
    org_id = app.current_event.get_header_value(name="X-Organization")
    org = auth0.organizations.get_organization(org_id)
    return {
        'id': org.get('id', ''),
        'name': org.get('name', ''),
        'display_name': org.get('display_name', ''),
    }


@app.get("/auth/v1/organizations/<organization_id>")
@tracer.capture_method
def get_organization(organization_id):
    org = auth0.organizations.get_organization(organization_id)
    logger.info(org)
    return org


@app.put("/auth/v1/organizations/<organization_id>")
@tracer.capture_method
def update_organization(organization_id):
    payload = app.current_event.json_body
    return auth0.organizations.update_organization(organization_id, payload)


@app.post("/auth/v1/organizations/<organization_id>/keys")
@tracer.capture_method
def create_organization_key(organization_id):

    # Check the org for the api key
    org = auth0.organizations.get_organization(organization_id)
    logger.info(org)

    metadata = org.get('metadata', {})
    api_key = metadata.get('api_key', None)

    # Create & save if it doesnt exist
    if not api_key:
        api_key = secrets.token_urlsafe(16)
        metadata['api_key'] = api_key
        payload = {'metadata': metadata}
        auth0.organizations.update_organization(organization_id, payload)

    # Return it
    return {'api_key': api_key}


@app.post("/auth/v1/organizations/<organization_id>/invitations")
@tracer.capture_method
def create_organization_invitation(organization_id):
    payload = app.current_event.json_body
    return auth0.organizations.create_organization_invitation(organization_id, payload)


@app.get("/auth/v1/organizations/<organization_id>/invitations")
@tracer.capture_method
def list_organization_invitations(organization_id):
    return auth0.organizations.all_organization_invitations(organization_id)


@app.get("/auth/v1/organizations/<organization_id>/members")
@tracer.capture_method
def list_organization_members(organization_id):
    return auth0.organizations.all_organization_members(organization_id)


@app.get("/auth/v1/organizations/<organization_id>/members/<user_id>/roles")
@tracer.capture_method
def list_organization_member_roles(organization_id, user_id):
    return auth0.organizations.all_organization_member_roles(organization_id, user_id)


@app.get("/auth/v1/users/<user_id>")
@tracer.capture_method
def get_user(user_id):
    user = auth0.users.get(user_id)
    user_organizations = auth0.users.list_organizations(user_id)
    user['organizations'] = user_organizations['organizations']
    return user


@app.put("/auth/v1/users/<user_id>")
@tracer.capture_method
def update_user(user_id):
    payload = app.current_event.json_body
    return auth0.users.update(user_id, payload)


@app.get("/auth/v1/users/<user_id>/organizations")
@tracer.capture_method
def list_user_organizations(user_id):
    return auth0.users.list_organizations(user_id)


@cors_headers()
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
