import os
import secrets

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.api_gateway import \
    APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from lambda_decorators import cors_headers

from ..utils.auth0 import auth0, generate_name_slug
from ..utils.stripe import BasicPackage, stripe

app = APIGatewayRestResolver(strip_prefixes=["/partners"])
logger = Logger()
tracer = Tracer()

"""
Organization Endpoints
"""


@app.post("/auth0/organizations")
@tracer.capture_method
def create_organization():
    payload = app.current_event.json_body
    authorizer = app.current_event.request_context.authorizer
    user_id = authorizer.get('user')

    # Create organization
    payload['name'] = generate_name_slug(payload['display_name'])
    org = auth0.organizations.create_organization(payload)

    # Enable connections
    payload = {
        "connection_id": os.environ['AUTH0_DB_CONNECTION'],
        "assign_membership_on_login": False
    }
    auth0.organizations.create_organization_connection(org['id'], payload)

    # Assign user to it
    payload = {'members': [user_id]}
    auth0.organizations.create_organization_members(org['id'], payload)

    # Add owner role to user
    payload = {'roles': [os.environ['AUTH0_OWNER_ROLE']]}
    auth0.organizations.create_organization_member_roles(
        org['id'], user_id, payload)

    # Create stripe customer for organization
    customer = stripe.Customer.create(
        description=org['display_name'],
        email=authorizer.get('email'),
        metadata={'organization': org['id']},
        name=org['display_name']
    )

    # Subscribe customer to free package
    subscription = stripe.Subscription.create(
        customer=customer['id'],
        items=[
            {'price': BasicPackage.PACKAGE_PRICE},
            {'price': BasicPackage.COLLECTION_PRICE},
            {'price': BasicPackage.MINT_PRICE},
        ]
    )

    # Create Public and Secret Keys for organization
    api_public_key = 'pk_' + secrets.token_urlsafe(16)
    api_secret_key = 'sk_' + secrets.token_urlsafe(16)

    # Save metadata to organization
    metadata = org.get('metadata', {})
    metadata['stripe_customer'] = customer['id']
    metadata['stripe_subscription'] = subscription['id']
    metadata['api_public_key'] = api_public_key
    metadata['api_secret_key'] = api_secret_key
    payload = {'metadata': metadata}
    org = auth0.organizations.update_organization(org['id'], payload)
    return org


@app.get("/auth0/organizations/<id>")
@tracer.capture_method
def get_organization(id):
    return auth0.organizations.get_organization(id)


@app.put("/auth0/organizations/<id>")
@tracer.capture_method
def update_organization(id):
    payload = app.current_event.json_body
    return auth0.organizations.update_organization(id, payload)


@app.post("/auth0/organizations/<id>/invitations")
@tracer.capture_method
def create_organization_invitation(id):
    payload = app.current_event.json_body
    return auth0.organizations.create_organization_invitation(id, payload)


@app.get("/auth0/organizations/<id>/invitations")
@tracer.capture_method
def list_organization_invitations(id):
    return auth0.organizations.all_organization_invitations(id)


@app.get("/auth0/organizations/<id>/members")
@tracer.capture_method
def list_organization_members(id):
    result = []
    members = auth0.organizations.all_organization_members(id)
    for member in members.get('members', []):
        user_id = member['user_id']
        roles = auth0.organizations.all_organization_member_roles(id, user_id)
        member['roles'] = roles
        result.append(member)
    return members


@app.get("/auth0/organizations/<id>/validate")
@tracer.capture_method
def validate_organization(id):
    return auth0.organizations.get_organization(id)


"""
User Endpoints
"""


@app.get("/auth0/users/<user_id>")
@tracer.capture_method
def get_user(user_id):
    user = auth0.users.get(user_id)
    user_organizations = auth0.users.list_organizations(user_id)
    user['organizations'] = user_organizations['organizations']
    return user


@app.put("/auth0/users/<user_id>")
@tracer.capture_method
def update_user(user_id):
    payload = app.current_event.json_body
    return auth0.users.update(user_id, payload)


@app.get("/auth0/users/<user_id>/organizations")
@tracer.capture_method
def list_user_organizations(user_id):
    return auth0.users.list_organizations(user_id)


@cors_headers
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context)
