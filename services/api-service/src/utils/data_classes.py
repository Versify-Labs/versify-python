from typing import Any, Dict, List, Optional

from versify import Versify

from .common import (BaseProxyEvent, BaseRequestContext, BaseRequestContextV2,
                     DictWrapper)

versify = Versify()


class APIGatewayEventAuthorizer(DictWrapper):
    @property
    def claims(self) -> Optional[Dict[str, Any]]:
        return self.get("claims")

    @property
    def scopes(self) -> Optional[List[str]]:
        return self.get("scopes")

    @property
    def principal_id(self) -> Optional[str]:
        """The principal user identification associated with the token sent by the client and returned from an
        API Gateway Lambda authorizer (formerly known as a custom authorizer)"""
        return self.get("principalId")

    @property
    def integration_latency(self) -> Optional[int]:
        """The authorizer latency in ms."""
        return self.get("integrationLatency")


class APIGatewayEventRequestContext(BaseRequestContext):
    @property
    def connected_at(self) -> Optional[int]:
        """The Epoch-formatted connection time. (WebSocket API)"""
        return self["requestContext"].get("connectedAt")

    @property
    def connection_id(self) -> Optional[str]:
        """A unique ID for the connection that can be used to make a callback to the client. (WebSocket API)"""
        return self["requestContext"].get("connectionId")

    @property
    def event_type(self) -> Optional[str]:
        """The event type: `CONNECT`, `MESSAGE`, or `DISCONNECT`. (WebSocket API)"""
        return self["requestContext"].get("eventType")

    @property
    def message_direction(self) -> Optional[str]:
        """Message direction (WebSocket API)"""
        return self["requestContext"].get("messageDirection")

    @property
    def message_id(self) -> Optional[str]:
        """A unique server-side ID for a message. Available only when the `eventType` is `MESSAGE`."""
        return self["requestContext"].get("messageId")

    @property
    def operation_name(self) -> Optional[str]:
        """The name of the operation being performed"""
        return self["requestContext"].get("operationName")

    @property
    def route_key(self) -> Optional[str]:
        """The selected route key."""
        return self["requestContext"].get("routeKey")

    @property
    def authorizer(self) -> APIGatewayEventAuthorizer:
        return APIGatewayEventAuthorizer(self._data["requestContext"]["authorizer"])


class APIGatewayProxyEvent(BaseProxyEvent):
    """AWS Lambda proxy V1

    Documentation:
    --------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """

    @property
    def version(self) -> str:
        return self["version"]

    @property
    def resource(self) -> str:
        return self["resource"]

    @property
    def multi_value_headers(self) -> Dict[str, List[str]]:
        return self["multiValueHeaders"]

    @property
    def multi_value_query_string_parameters(self) -> Optional[Dict[str, List[str]]]:
        return self.get("multiValueQueryStringParameters")

    @property
    def request_context(self) -> APIGatewayEventRequestContext:
        return APIGatewayEventRequestContext(self._data)

    @property
    def path_parameters(self) -> Optional[Dict[str, str]]:
        return self.get("pathParameters")

    @property
    def stage_variables(self) -> Optional[Dict[str, str]]:
        return self.get("stageVariables")


class RequestContextV2AuthorizerIam(DictWrapper):
    @property
    def access_key(self) -> Optional[str]:
        """The IAM user access key associated with the request."""
        return self.get("accessKey")

    @property
    def account_id(self) -> Optional[str]:
        """The AWS account ID associated with the request."""
        return self.get("accountId")

    @property
    def caller_id(self) -> Optional[str]:
        """The principal identifier of the caller making the request."""
        return self.get("callerId")

    @property
    def cognito_amr(self) -> Optional[List[str]]:
        """This represents how the user was authenticated.
        AMR stands for  Authentication Methods References as per the openid spec"""
        return self["cognitoIdentity"].get("amr")

    @property
    def cognito_identity_id(self) -> Optional[str]:
        """The Amazon Cognito identity ID of the caller making the request.
        Available only if the request was signed with Amazon Cognito credentials."""
        return self["cognitoIdentity"].get("identityId")

    @property
    def cognito_identity_pool_id(self) -> Optional[str]:
        """The Amazon Cognito identity pool ID of the caller making the request.
        Available only if the request was signed with Amazon Cognito credentials."""
        return self["cognitoIdentity"].get("identityPoolId")

    @property
    def principal_org_id(self) -> Optional[str]:
        """The AWS organization ID."""
        return self.get("principalOrgId")

    @property
    def user_arn(self) -> Optional[str]:
        """The Amazon Resource Name (ARN) of the effective user identified after authentication."""
        return self.get("userArn")

    @property
    def user_id(self) -> Optional[str]:
        """The IAM user ID of the effective user identified after authentication."""
        return self.get("userId")


class RequestContextV2Authorizer(DictWrapper):
    @property
    def jwt_claim(self) -> Dict[str, Any]:
        return self["jwt"]["claims"]

    @property
    def jwt_scopes(self) -> List[str]:
        return self["jwt"]["scopes"]

    @property
    def get_lambda(self) -> Optional[Dict[str, Any]]:
        """Lambda authorization context details"""
        return self.get("lambda")

    @property
    def iam(self) -> Optional[RequestContextV2AuthorizerIam]:
        """IAM authorization details used for making the request."""
        iam = self.get("iam")
        return None if iam is None else RequestContextV2AuthorizerIam(iam)


class RequestContextV2(BaseRequestContextV2):
    @property
    def authorizer(self) -> Optional[RequestContextV2Authorizer]:
        authorizer = self["requestContext"].get("authorizer")
        return None if authorizer is None else RequestContextV2Authorizer(authorizer)


class APIGatewayProxyEventV2(BaseProxyEvent):
    """AWS Lambda proxy V2 event

    Notes:
    -----
    Format 2.0 doesn't have multiValueHeaders or multiValueQueryStringParameters fields. Duplicate headers
    are combined with commas and included in the headers field. Duplicate query strings are combined with
    commas and included in the queryStringParameters field.

    Format 2.0 includes a new cookies field. All cookie headers in the request are combined with commas and
    added to the cookies field. In the response to the client, each cookie becomes a set-cookie header.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    """

    @property
    def version(self) -> str:
        return self["version"]

    @property
    def route_key(self) -> str:
        return self["routeKey"]

    @property
    def raw_path(self) -> str:
        return self["rawPath"]

    @property
    def raw_query_string(self) -> str:
        return self["rawQueryString"]

    @property
    def cookies(self) -> Optional[List[str]]:
        return self.get("cookies")

    @property
    def request_context(self) -> RequestContextV2:
        return RequestContextV2(self._data)

    @property
    def path_parameters(self) -> Optional[Dict[str, str]]:
        return self.get("pathParameters")

    @property
    def stage_variables(self) -> Optional[Dict[str, str]]:
        return self.get("stageVariables")

    @property
    def path(self) -> str:
        stage = self.request_context.stage
        if stage != "$default":
            return self.raw_path[len("/" + stage):]
        return self.raw_path

    @property
    def http_method(self) -> str:
        """The HTTP method used. Valid values include: DELETE, GET, HEAD, OPTIONS, PATCH, POST, and PUT."""
        return self.request_context.http.method


class User:

    def __init__(self, id=None, email=None, name=None, accounts=None):
        self.id = id
        self.email = email
        self.name = name
        self.accounts = accounts or []

    def __repr__(self):
        return f'User({self.id}, { self.email}, {self.name}, {self.accounts})'

    def __eq__(self, other):
        return self.id == other.id and self.email == other.email and self.name == other.name and self.accounts == other.accounts

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.id, self.email, self.name, tuple(self.accounts)))

    def __str__(self):
        return self.__repr__()

    @property
    def account_ids(self):
        return [account.id for account in self.accounts]


class Account:

    def __init__(self, id=None, name=None, team=None):
        self.id = id
        self.name = name
        self.team = team or []

    def __repr__(self):
        return f'Account({self.id},
    
    def save_




class Identity:

    def __init__(self, auth_type=None, auth_token=None):
        self._account_id = None
        self._account = None
        self._user_id = None
        self._email = None
        self._user = {}
        self._roles = []

        if not auth_type or not auth_token:
            return

        # TODO: Validate the access token

        # Get the user info from the access token
        user = versify.user_service.get_user_by_token(auth_token)
        if user:
            self.user = user

        # Create a set of roles from the user info
        if user:
            for account in user.get('accounts', []):
                account_id = account.get('id')
                for team_member in account.get('team', []):
                    if team_member.get('email') == user.get('email'):
                        role_name = team_member.get('role', 'member')
                        self.roles.append(f'{account_id}:{role_name}')

    def set_account(self, account_id):
        """Set the current account for the user."""
        self.account_id = account_id

    @property
    def is_active(self) -> bool:
        """Return True if the effective user identified after authentication is active."""
        return self.user.get('active', False)

    @property
    def email(self) -> Optional[str]:
        """The email address of the effective user identified after authentication."""
        return self.user.get('email')

    @property
    def user_id(self) -> Optional[str]:
        """The user ID of the effective user identified after authentication."""
        return self.user.get('id')

    def has_role(self, role):
        """Return True if the effective user identified after authentication has the specified role."""
        return role in self.roles

    def has_account_role(self, account_id, role):
        """Return True if the effective user identified after authentication has the specified role."""
        return self.has_role(f'{account_id}:{role}')

    def has_account_access(self, account_id, roles_required):
        """Return True if the effective user identified after authentication has any of the specified roles."""
        return any([self.has_role(f'{account_id}:{role}') for role in roles_required])

    def has_account_subscription(self, account_id, plans_required):
        """Return True if the effective user identified after authentication has any of the specified plans."""
        accounts = self.user.get('accounts', [])
        for account in accounts:
            if account.get('id') == account_id:
                billing = account.get('billing', {})
                return billing.get('subscription_plan', 'trial') in plans_required
        return False

    def has_access(self, account_id, roles_required=['admin', 'member'], plans_required=['trial', 'growth', 'enterprise']):
        """Return True if the effective identity has the required roles and plans."""

        # - Check if the user is active
        if not self.is_active:
            return False, 'User is not active'

        # - Check if the user belongs to the account
        # - Check if the user has one of the following roles: 'admin', 'member'
        if not self.has_account_access(account_id, roles_required):
            return False, 'User role must be one of the following: ' + ', '.join(roles_required)

        # - Check if the account is active
        # - Check if the account has an active subscription
        # - Check if the account has one of the following subscription plans: 'trial', 'growth', 'enterprise'
        if not self.has_account_subscription(account_id, plans_required):
            return False, 'Account subscription must be one of the following: ' + ', '.join(plans_required)

        return True, None
