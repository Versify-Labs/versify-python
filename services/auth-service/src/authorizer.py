import json
import os
import urllib.request

from aws_lambda_powertools import Logger, Tracer
from jose import jwt

from .auth0 import init_auth0

tracer = Tracer()
logger = Logger()

if os.environ['ENVIRONMENT'] == 'dev':
    AUTH0_DOMAIN = 'dev-4grvkowo.us.auth0.com'
    VERSIFY_API = 'https://api.dev.versifylabs.com/admin'
else:
    AUTH0_DOMAIN = 'versify.us.auth0.com'
    VERSIFY_API = 'https://api.versifylabs.com/admin'
ALGORITHMS = ["RS256"]
AUTH0_PUBLIC_KEY_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
REGION = os.environ['AWS_REGION']

auth0 = init_auth0()


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
    return value


def is_valid_token(token):
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
    return True if rsa_key else False


def is_valid_org_key(api_key, organization):
    """Determines if the api_key has access to the organization requested in the header"""
    org = auth0.organizations.get_organization(organization)
    metadata = org.get('metadata', {})
    true_key = metadata.get('api_key', None)
    if not true_key:
        return False
    return api_key == true_key


def create_principal_id(api_key=None, token=None, organization=None):
    principal = ''
    if api_key:
        principal = api_key
    if organization:
        principal = organization
    if token:
        claims = jwt.get_unverified_claims(token)
        principal = claims.get('sub')
    return principal


def create_auth_context(api_key=None, token=None, organization=None):
    context = {}
    namespace = 'https://versifylabs.com'
    if organization:
        context['organization'] = organization
    if token:
        claims = jwt.get_unverified_claims(token)
        logger.info(claims)
        context['email'] = claims.get(f'{namespace}/email')
        context['roles'] = ','.join(claims.get(f'{namespace}/roles') or [])
        context['user'] = claims.get('sub')
    return context


def get_requested_scope(event):
    api_method = event['httpMethod']
    method_map = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'PATCH': 'write',
        'DELETE': 'write'
    }
    access = method_map[api_method]
    requested_path = event['path']
    requested_path_segments = requested_path.split('/')
    resource = requested_path_segments[3]
    if '_' in resource:
        resource = resource.split('_')[0] + 's'
    return f'{access}:{resource}'


def handle_key(api_key=None, organization=None):
    if not api_key or not organization:
        logger.info('Missing key / organization')
        return False
    return is_valid_org_key(api_key, organization)


def handle_token(scope, token=None, organization=None):
    if not token:
        logger.info('Missing token')
        return False

    claims = jwt.get_unverified_claims(token)
    logger.info(claims)

    # Validate token
    if not is_valid_token(token):
        logger.info('Invalid token')
        return False

    # Validate scope in token
    if scope not in claims.get('permissions', []):
        logger.info('Invalid permissions')
        return False

    # Validate organization in token
    if organization and claims.get('org_id'):
        if claims.get('org_id') != organization:
            logger.info('Invalid organization')
            return False

    return True


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def handler(event, context):
    key = get_header_value(event, 'x-api-key')
    organization = get_header_value(event, 'x-organization')
    token = get_header_value(event, 'x-authorization')
    token = token.split(' ')[1] if token and token != '' else None
    scope = get_requested_scope(event)
    logger.info({
        'key': key,
        'token': token,
        'organization': organization,
        'scope': scope
    })

    valid_key = handle_key(key, organization)
    valid_token = handle_token(scope, token, organization)
    logger.info({
        'Valid key': valid_key,
        'Valid token': valid_token
    })

    method_arn = event['methodArn']
    principal_id = create_principal_id(key, token, organization)
    auth_context = create_auth_context(key, token, organization)
    logger.info(principal_id)
    logger.info(auth_context)

    if not (valid_key or valid_token):
        return generate_deny(principal_id, method_arn)
    return generate_allow(principal_id, method_arn, auth_context)
