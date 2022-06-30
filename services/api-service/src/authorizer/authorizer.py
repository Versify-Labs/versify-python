import json
import os
import urllib.request

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


class Authorizer:

    def __init__(self, user=None, organization=None):
        self.user = user
        self.organization = organization

    def list_org_permissions(self):
        pass

    def list_user_permissions(self):
        pass

    def create_principal_id(self, api_key=None, token=None, organization=None):
        principal = ''
        if api_key:
            principal = api_key
        if organization:
            principal = organization
        if token:
            claims = jwt.get_unverified_claims(token)
            principal = claims.get('sub')
        return principal

    def create_auth_context(self, api_key=None, token=None, organization=None):
        context = {}

        if token:
            claims = jwt.get_unverified_claims(token)
            logger.info(claims)

            context['email'] = claims.get(f'{NAMESPACE}/email')
            context['roles'] = ','.join(claims.get(f'{NAMESPACE}/roles') or [])
            context['permissions'] = ','.join(
                claims.get(f'{NAMESPACE}/permissions') or [])
            context['user'] = claims.get('sub')

            organization = claims.get(f'{NAMESPACE}/organization')
            if organization:
                organization_id = organization.get('id', '')
                metadata = organization.get('metadata', {})
                stripe_customer = metadata.get('stripe_customer', '')
                context['organization'] = organization_id
                context['stripe_customer'] = stripe_customer

        return context

    def generate_policy(self, principalId, effect, resource, context={}):
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

    def generate_allow(self, principalId, resource, context):
        return self.generate_policy(principalId, 'Allow', resource, context)

    def generate_deny(self, principalId, resource):
        return self.generate_policy(principalId, 'Deny', resource)


class KeyAuthorizer(Authorizer):

    def __init__(self, api_key, organization):
        self.api_key = api_key
        super().__init__(organization=organization)

    def is_valid_org_key(self, api_key, organization):
        """Determines if the api_key has access to the organization requested in the header"""
        org = auth0.organizations.get_organization(organization)
        metadata = org.get('metadata', {})
        true_key = metadata.get('api_key', None)
        if not true_key:
            return False
        return api_key == true_key

    def authorize(self, event):
        if not self.api_key:
            return self.generate_deny()


class TokenAuthorizer(Authorizer):

    def __init__(self, token, organization):
        self.token = token
        super().__init__(organization=organization)

    def is_valid_token(self):
        """Determines if the token is valid"""
        jsonurl = urllib.request.urlopen(AUTH0_PUBLIC_KEY_URL)
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(self.token)
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



    def authorize(self, event):

        # Validate token with Auth0
        if not self.is_valid_token():
            return self.generate_deny()

        # Get requested scope for the user / org
        scope = self.get_requested_scope()

        # Validate requested scope is within users permissions
