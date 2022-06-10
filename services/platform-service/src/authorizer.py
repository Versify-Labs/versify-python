import json
import os
import urllib.request

from aws_lambda_powertools import Logger, Tracer
from jose import jwt

tracer = Tracer()
logger = Logger()

if os.environ['ENVIRONMENT'] == 'dev':
    AUTH0_DOMAIN = 'dev-4grvkowo.us.auth0.com'
    VERSIFY_ACCOUNT_API = 'https://api.dev.versifylabs.com/account'
    VERSIFY_ADMIN_API = 'https://api.dev.versifylabs.com/admin'
else:
    AUTH0_DOMAIN = 'versify.us.auth0.com'
    VERSIFY_ACCOUNT_API = 'https://api.versifylabs.com/account'
    VERSIFY_ADMIN_API = 'https://api.versifylabs.com/admin'
ALGORITHMS = ["RS256"]
AUTH0_PUBLIC_KEY_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
REGION = os.environ['AWS_REGION']


def generate_policy(principalId, effect, resource, context={}):
    auth_response = {}
    auth_response['principalId'] = principalId
    if effect and resource:
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = [statementOne]
        auth_response['policyDocument'] = policyDocument
    auth_response['context'] = context
    logger.info(auth_response)
    return auth_response


def generate_allow(principalId, resource, context):
    return generate_policy(principalId, 'Allow', resource, context)


def generate_deny(principalId, resource):
    return generate_policy(principalId, 'Deny', resource)


def get_header_value(event, key):
    headers = {k.lower(): v for k, v in event['headers'].items()}
    value = headers.get(key)
    logger.info({
        'key': key,
        'value': value
    })
    return value


def get_required_scope(event):
    api_method = event['httpMethod']
    api_resource = event['resource']
    method_map = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'PATCH': 'write',
        'DELETE': 'write'
    }
    resource_map = {
        '/admin/airdrops': 'airdrops',
        '/admin/events': 'events',
        '/admin/events/{id}': 'events',
        '/admin/orders': 'orders',
        '/admin/orders/{id}': 'orders',
        '/admin/orders/{id}/fulfillments': 'orders',
        '/admin/notifications': 'notifications',
        '/admin/notifications/{id}': 'notifications',

        '/auth/v1/ping': 'organizations',
        '/auth/v1/organizations': 'organizations',
        '/auth/v1/organizations/{organization_id}': 'organizations',
        '/auth/v1/organizations/{organization_id}/keys': 'organizations',
        '/auth/v1/organizations/{organization_id}/keys/{user_id}': 'organizations',
        '/auth/v1/organizations/{organization_id}/members': 'organizations',
        '/auth/v1/organizations/{organization_id}/members/{user_id}': 'organizations',
        '/auth/v1/organizations/{organization_id}/members/{user_id}/roles': 'organizations',
        '/auth/v1/users/{user_id}': 'organizations',
        '/auth/v1/users/{user_id}/organizations': 'organizations',

        '/billing/v1/invoice': 'organizations',
        '/billing/v1/invoice/{invoice_id}': 'organizations',
        '/billing/v1/plan': 'organizations',
        '/billing/v1/plan/{plan_id}': 'organizations',
        '/billing/v1/subscription': 'organizations',
        '/billing/v1/subscription/{subscription_id}': 'organizations',
        '/billing/v1/usage': 'organizations',
        '/billing/v1/usage/{usage_id}': 'organizations',

        '/cms/v1/pages': 'organizations',
        '/cms/v1/pages/{page_id}': 'organizations',

        '/crm/v1/contacts': 'organizations',
        '/crm/v1/contacts/{contact_id}': 'organizations',
        '/crm/v1/contacts/{contact_id}/activity': 'organizations',
        '/crm/v1/contacts/{contact_id}/activity/{activity_id}': 'organizations',
        '/crm/v1/contacts/{contact_id}/actions/archive': 'organizations',
        '/crm/v1/contacts/{contact_id}/notes': 'organizations',
        '/crm/v1/contacts/{contact_id}/notes/{note_id}': 'organizations',
        '/crm/v1/contacts/{contact_id}/tags': 'organizations',
        '/crm/v1/contacts/{contact_id}/tags/{tag_id}': 'organizations',
        '/crm/v1/tags': 'organizations',
        '/crm/v1/tags/{tag_id}': 'organizations',

        '/oms/v1/airdrops': 'organizations',
        '/oms/v1/airdrops/{airdrop_id}': 'organizations',
        '/oms/v1/orders': 'organizations',
        '/oms/v1/orders/{collection_id}': 'organizations',

        '/pim/v1/collections': 'organizations',
        '/pim/v1/collections/{collection_id}': 'organizations',
        '/pim/v1/collections/{collection_id}/actions/archive': 'organizations',
        '/pim/v1/collections/{collection_id}/actions/publish': 'organizations',
        '/pim/v1/collections/{collection_id}/actions/unarchive': 'organizations',
        '/pim/v1/products': 'organizations',
        '/pim/v1/products/{product_id}': 'organizations',
        '/pim/v1/products/{product_id}/actions/archive': 'organizations',
        '/pim/v1/products/{product_id}/actions/publish': 'organizations',
        '/pim/v1/products/{product_id}/actions/unarchive': 'organizations',

        '/blockchain/v1/transactions': 'organizations',
        '/blockchain/v1/transactions/{transaction_id}': 'organizations',

    }
    access = method_map[api_method]
    resource = resource_map[api_resource]
    return f'{access}:{resource}'


def is_valid_api_key(api_key, organization):
    """Determines if the api_key has access to the organization requested in the header"""
    # TODO: Match up API key with Organization
    return api_key == f'{organization}_superSecretKey'


def is_valid_token(token, audience):
    """Determines if the token is valid"""
    jsonurl = urllib.request.urlopen(AUTH0_PUBLIC_KEY_URL)
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    logger.info(rsa_key)
    if not rsa_key:
        return False
    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=audience,
        issuer="https://"+AUTH0_DOMAIN+"/"
    )
    logger.info(payload)
    return True


def is_valid_scope(token, required_scope):
    """Determines if the required scope is present in the Access Tokens scope"""
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def is_valid_permission(token, required_scope):
    """Determines if the required scope is present in the Access Tokens permission"""
    unverified_claims = jwt.get_unverified_claims(token)
    permissions = unverified_claims.get('permissions', [])
    return required_scope in permissions


def is_valid_organization(token, organization):
    """Determines if the Access Token has access to the organization requested in the header"""
    unverified_claims = jwt.get_unverified_claims(token)
    return organization == unverified_claims.get("org_id")


def account_token_auth(token, scope, resource):
    claims = jwt.get_unverified_claims(token)
    user_id = claims.get('sub')
    audience = VERSIFY_ACCOUNT_API

    if not is_valid_token(token, audience):
        logger.info('Invalid Token')
        return generate_deny(user_id, resource)

    if not is_valid_scope(token, scope) and not is_valid_permission(token, scope):
        logger.info('Invalid Permissions')
        return generate_deny(user_id, resource)

    # Congrats! You are authorized!
    auth_context = {'user_id': user_id}
    return generate_allow(user_id, resource, auth_context)


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def account_handler(event, context):

    # Who are you?
    token = get_header_value(event, 'x-authorization')
    token = token.split(' ')[1]

    # What are you requesting?
    resource = event['methodArn']
    scope = get_required_scope(event)

    # Determine if auth type is API Key or Access Token and check if has access
    if token:
        return account_token_auth(token, scope, resource)
    else:
        return generate_deny('unknown', resource)


def admin_token_auth(token, organization, scope, resource):
    token = token.split(' ')[1]
    claims = jwt.get_unverified_claims(token)
    user_id = claims.get('sub')
    audience = VERSIFY_ADMIN_API

    if not is_valid_token(token, audience):
        logger.info('Invalid Token')
        return generate_deny(user_id, resource)

    if not is_valid_organization(token, organization):
        logger.info('Invalid Organization')
        return generate_deny(user_id, resource)

    # TODO: VALIDATE THAT THE ORGANIZATION PLAN HAS ACCESS TO THE SCOPE
    if not is_valid_scope(token, scope) and not is_valid_permission(token, scope):
        logger.info('Invalid Permissions')
        return generate_deny(user_id, resource)

    # Congrats! You are authorized!
    auth_context = {'user_id': user_id,  'org_id': organization}
    return generate_allow(user_id, resource, auth_context)


def admin_api_key_auth(api_key, organization, scope, resource):

    if not is_valid_api_key(api_key, organization):
        logger.info('Invalid API Key')
        return generate_deny(organization, resource)

    # TODO: VALIDATE THAT THE ORGANIZATION PLAN HAS ACCESS TO THE SCOPE

    # Should you have access to what you are requesting?
    # TODO: Check that Organization has granted API Key permission to this specific scope

    # Congrats! You are authorized!
    auth_context = {'org_id': organization}
    return generate_allow(organization, resource, auth_context)


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def admin_handler(event, context):

    # Who are you?
    api_key = get_header_value(event, 'x-api-key')
    token = get_header_value(event, 'x-authorization')

    # What are you requesting?
    organization = get_header_value(event, 'x-organization')
    resource = event['methodArn']
    scope = get_required_scope(event)

    # Determine if auth type is API Key or Access Token and check if has access
    if api_key and organization:
        return admin_api_key_auth(api_key, organization, scope, resource)
    elif token and organization:
        return admin_token_auth(token, organization, scope, resource)
    else:
        return generate_deny('unknown', resource)
