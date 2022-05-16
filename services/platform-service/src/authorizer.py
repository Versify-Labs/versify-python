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


def get_token(event):
    authorization_lo = event['headers'].get('authorization')
    authorization_up = event['headers'].get('Authorization')
    authorization = authorization_lo or authorization_up
    token = authorization.split(' ')[1]
    return token


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
        '/account/integrations/auth0/users/{id}/organizations': 'organizations',
        '/admin/airdrops': 'airdrops',
        '/admin/collections': 'collections',
        '/admin/collections/{id}': 'collections',
        '/admin/customers': 'customers',
        '/admin/customers/{id}': 'customers',
        '/admin/events': 'events',
        '/admin/events/{id}': 'events',
        '/admin/integrations/auth0/organizations/{id}': 'organizations',
        '/admin/integrations/auth0/organizations/{id}/invitations': 'organizations',
        '/admin/integrations/auth0/organizations/{id}/members': 'organizations',
        '/admin/integrations/auth0/organizations/{id}/members/{user_id}/roles': 'organizations',
        '/admin/orders': 'orders',
        '/admin/orders/{id}': 'orders',
        '/admin/orders/{id}/fulfillments': 'orders',
        '/admin/products': 'products',
        '/admin/products/{id}': 'products',
        '/admin/notifications': 'notifications',
        '/admin/notifications/{id}': 'notifications',
    }
    access = method_map[api_method]
    resource = resource_map[api_resource]
    return f'{access}:{resource}'


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
    """Determines if the organization requested in the header is in the Access Token"""
    unverified_claims = jwt.get_unverified_claims(token)
    return organization == unverified_claims.get("org_id")


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def account_handler(event, context):

    # Who are you?
    token = get_token(event)
    unverified_claims = jwt.get_unverified_claims(token)
    user_id = unverified_claims.get('sub')
    if not token:
        logger.info('Missing Token')
        return generate_deny(user_id, event['methodArn'])

    # But are you really them?
    audience = VERSIFY_ACCOUNT_API
    if not is_valid_token(token, audience):
        logger.info('Invalid Token')
        return generate_deny(user_id, event['methodArn'])

    # What are your requesting?
    required_scope = get_required_scope(event)

    # Should you have access to what you are requesting?
    # TODO: Implement adding role (User) inside Auth0 Rule
    # if not is_valid_scope(token, required_scope) and not is_valid_permission(token, required_scope):
    #     logger.info('Invalid Permissions')
    #     return generate_deny(user_id, event['methodArn'])

    # Congrats! You are authorized!
    unverified_claims = jwt.get_unverified_claims(token)
    auth_context = {
        'user_id': unverified_claims.get('sub'),
        'org_id': unverified_claims.get('org_id')
    }
    user_id = unverified_claims.get('sub')
    return generate_allow(user_id, event['methodArn'], auth_context)


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def admin_handler(event, context):

    # Who are you?
    token = get_token(event)
    unverified_claims = jwt.get_unverified_claims(token)
    user_id = unverified_claims.get('sub')
    if not token:
        logger.info('Missing Token')
        return generate_deny(user_id, event['methodArn'])

    # But are you really them?
    audience = VERSIFY_ADMIN_API
    if not is_valid_token(token, audience):
        logger.info('Invalid Token')
        return generate_deny(user_id, event['methodArn'])

    # What are your requesting?
    required_scope = get_required_scope(event)

    # Are you requesting on behalf of an organization?
    organization_lo = event['headers'].get('organization')
    organization_up = event['headers'].get('Organization')
    organization = organization_lo or organization_up
    if organization and not is_valid_organization(token, organization):
        logger.info('Invalid Organization')
        return generate_deny(user_id, event['methodArn'])

    # TODO: VALIDATE THAT THE ORGANIZATION PLAN HAS ACCESS TO THE SCOPE

    # Should you have access to what you are requesting?
    if not is_valid_scope(token, required_scope) and not is_valid_permission(token, required_scope):
        logger.info('Invalid Permissions')
        return generate_deny(user_id, event['methodArn'])

    # Congrats! You are authorized!
    unverified_claims = jwt.get_unverified_claims(token)
    auth_context = {
        'user_id': unverified_claims.get('sub'),
        'org_id': unverified_claims.get('org_id')
    }
    user_id = unverified_claims.get('sub')
    return generate_allow(user_id, event['methodArn'], auth_context)
