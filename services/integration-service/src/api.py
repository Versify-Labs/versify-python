import http.client
import json
import os

from auth0.v3.management import Auth0
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities import parameters
from lambda_decorators import cors_headers

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

SECRET_NAME = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET_NAME)
AUTH0_DOMAIN = SECRET['AUTH0_DOMAIN']
AUTH0_M2M_CLIENT_ID = SECRET['AUTH0_M2M_CLIENT_ID']
AUTH0_M2M_CLIENT_SECRET = SECRET['AUTH0_M2M_CLIENT_SECRET']
AUTH0_MGMT_API_AUDIENCE = f'https://{AUTH0_DOMAIN}/api/v2/'
AUTH0_MGMT_API_BASE_URL = f"https://{AUTH0_DOMAIN}"


def init_auth0():
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_M2M_CLIENT_ID,
        "client_secret": AUTH0_M2M_CLIENT_SECRET,
        "audience": AUTH0_MGMT_API_AUDIENCE
    }
    headers = {'content-type': "application/json"}
    conn.request(
        method="POST",
        url="/oauth/token",
        body=json.dumps(payload),
        headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    access_token = data.get('access_token')
    auth0 = Auth0(AUTH0_DOMAIN, access_token)
    return auth0


@app.get("/admin/integrations/auth0/organizations/<id>")
@tracer.capture_method
def get_organization(id):
    auth0 = init_auth0()
    return auth0.organizations.get_organization(id)


@app.get("/backend/organizations/<id>")
@tracer.capture_method
def get_organization(id):
    auth0 = init_auth0()
    return auth0.organizations.get_organization(id)


@app.put("/admin/integrations/auth0/organizations/<id>")
@tracer.capture_method
def update_organization(id):
    auth0 = init_auth0()
    payload = app.current_event.json_body
    return auth0.organizations.update_organization(id, payload)


@app.post("/admin/integrations/auth0/organizations/<id>/invitations")
@tracer.capture_method
def create_organization_invitation(id):
    auth0 = init_auth0()
    payload = app.current_event.json_body
    return auth0.organizations.create_organization_invitation(id, payload)


@app.get("/admin/integrations/auth0/organizations/<id>/invitations")
@tracer.capture_method
def list_organization_invitations(id):
    auth0 = init_auth0()
    return auth0.organizations.all_organization_invitations(id)


@app.get("/admin/integrations/auth0/organizations/<id>/members")
@tracer.capture_method
def list_organization_members(id):
    auth0 = init_auth0()
    return auth0.organizations.all_organization_members(id)


@app.get("/admin/integrations/auth0/organizations/<id>/members/<user_id>/roles")
@tracer.capture_method
def list_organization_member_roles(id, user_id):
    auth0 = init_auth0()
    return auth0.organizations.all_organization_member_roles(id, user_id)


@app.get("/account/integrations/auth0/users/<id>/organizations")
@tracer.capture_method
def list_user_organizations(id):
    auth0 = init_auth0()
    return auth0.users.list_organizations(id)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
