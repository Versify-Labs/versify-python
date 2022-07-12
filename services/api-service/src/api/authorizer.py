import os

from aws_lambda_powertools import Logger, Tracer
from jose import jwt

from ..utils.auth0 import init_auth0

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
NAMESPACE = 'https://versifylabs.com'

auth0 = init_auth0()


def get_header_value(event, key):
    headers = {k.lower(): v for k, v in event['headers'].items()}
    value = headers.get(key)
    return value


def get_requesting_principal(api_key=None, token=None, organization=None):
    if api_key and organization:
        org = auth0.organizations.get_organization(organization)
        metadata = org.get('metadata', {})
        true_key = metadata.get('api_secret_key', None)
        if true_key and true_key == api_key:
            return organization
    if token:
        claims = jwt.get_unverified_claims(token)
        return claims.get('sub')
    return None


def get_requested_scope(method, path, token=None, organization=None):
    """
    Return format:
    {owner}:{action}:{resource}

    User endpoint example:
    user_123:read:organizations

    Organization endpoint example:
    org_123:read:contacts
    """

    # Get owner of the resource
    owner = None
    if organization:
        owner = organization
    else:
        claims = jwt.get_unverified_claims(token)
        owner = claims.get('sub')

    # Get action to be performed on the resource
    method_map = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'write',
        'PATCH': 'write',
        'DELETE': 'write'
    }
    action = method_map[method]

    # Get resource
    requested_path_segments = path.split('/')
    logger.info(requested_path_segments)

    if requested_path_segments[1] == 'partners':
        resource = requested_path_segments[3]
    else:
        resource = requested_path_segments[2]

    return f'{owner}:{action}:{resource}'


# def list_user_permissions(user_id, token):
#     result = []

#     # Add user permissions
#     claims = jwt.get_unverified_claims(token)
#     user_perms = claims.get('permissions')
#     for perm_name in user_perms:
#         result.append(f'{user_id}:{perm_name}')

#     # Add org permissions
#     orgs = auth0.users.list_organizations(user_id)
#     for org in orgs['organizations']:
#         org_id = org['id']
#         roles = auth0.organizations.all_organization_member_roles(
#             org_id, user_id)
#         for role in roles:
#             role_id = role['id']
#             perms = auth0.roles.list_permissions(role_id, per_page=100)
#             for perm in perms['permissions']:
#                 perm_name = perm['permission_name']
#                 result.append(f'{org_id}:{perm_name}')

#     return result


def principal_has_access(principal, scope, token=None):

    # Handle API key calls
    if principal.startswith('org_'):
        return scope.startswith(principal)

    # Handle token calls
    # TODO: Validate token with Auth0
    # TODO: Check role permissions
    claims = jwt.get_unverified_claims(token)
    roles = claims.get(NAMESPACE + '/roles', [])
    for owner_role in roles:
        owner, role = owner_role.split(':')
        if scope.startswith(owner):
            return True

    return False


def create_auth_context(token=None, organization=None):
    context = {}
    if token:
        claims = jwt.get_unverified_claims(token)
        context['user'] = claims.get('sub')
        logger.info(claims)
    if organization:
        context['organization'] = organization
    return context


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


@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler
def handler(event, context):

    # Parse request
    method = event['httpMethod']
    method_arn = event['methodArn']
    path = event['path']
    key = get_header_value(event, 'x-api-key')
    organization = get_header_value(event, 'x-organization')
    token = get_header_value(event, 'x-authorization')
    token = token.split(' ')[1] if token and token != '' else None

    # Determine who is making the request (user or org)
    principal = get_requesting_principal(key, token, organization)
    if not principal:
        logger.error({
            'message': 'Could not identify principal',
            'key': key,
            'token': token,
            'organization': organization
        })
        return generate_deny(principal, method_arn)

    # Determine what they are requesting access to (user or org endpoint)
    scope = get_requested_scope(method, path, token, organization)
    if not scope:
        logger.error({
            'message': 'Could not identify scope',
            'method': method,
            'path': path,
            'token': token,
            'organization': organization
        })
        return generate_deny(principal, method_arn)

    logger.info({
        'principal': principal,
        'scope': scope
    })

    # Determine if the principal has access to the scope
    if not principal_has_access(principal, scope, token):
        logger.error({
            'message': 'Principal does not have access to scope',
            'principal': principal,
            'scope': scope
        })
        return generate_deny(principal, method_arn)

    context = create_auth_context(token, organization)
    return generate_allow(principal, method_arn, context)
