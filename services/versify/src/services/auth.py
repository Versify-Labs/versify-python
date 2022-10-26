"""Can authenticate an API call with a token and account id."""
import json
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters
from jose import jwt

from ..api.errors import NotFoundError
from ..utils.stytch import stytch

logger = Logger()
tracer = Tracer()


class AuthService:

    def __init__(
        self,
        account_service,
        user_service
    ) -> None:
        self.account_service = account_service
        self.user_service = user_service

    def get_paragon_api_key(self):
        secret_name = os.environ['SECRET_NAME']
        secret_raw = parameters.get_secret(secret_name)
        secret = json.loads(secret_raw)  # type: ignore
        paragon_sk = secret['PARAGON_SECRET_KEY']
        return paragon_sk

    def get_user_by_token(self, token: str):
        """Get a user by token.

        Args:
            token (str): The token to retrieve.

        Returns:
            dict: The user.
        """
        if not token:
            return

        try:
            claims = jwt.get_unverified_claims(token)
        except jwt.JWTError:  # type: ignore
            return
        if not claims:
            return

        session = claims.get('https://stytch.com/session')
        if not session:
            return

        stytch_user_id = claims.get('sub')
        if not stytch_user_id:
            return

        # Build user object
        auth_factors = session.get('authentication_factors', [])
        user_body = {'stytch_user': stytch_user_id}
        for factor in auth_factors:

            # Handle Magic Link session
            if factor.get('type') == 'magic_link':
                email_factor = factor.get('email_factor', {})
                user_body['email'] = email_factor.get('email_address')

            # Handle Oauth session
            if factor.get('type') == 'oauth':
                user = stytch().get_user(stytch_user_id)

                # user_body['avatar'] = user['providers'][0]['profile_picture_url']
                user_body['email'] = user['emails'][0]['email']
                user_body['first_name'] = user['name'].get('first_name')
                user_body['last_name'] = user['name'].get('last_name')

        return self.user_service.sync(user_body)

    def authenticate_account_api_key(self, api_key: str):
        """Authenticate an account using an API key.

        Args:
            api_key (str): The API key to authenticate with.

        Returns:
            success: Whether the authentication was successful.
            account: The account document if authentication was successful.
            error: The error message if authentication failed.
        """
        try:
            account = self.account_service.retrieve_by_api_secret_key(api_key)
        except NotFoundError:
            return False, None, 'Invalid API key'
        return True, account, None

    def authenticate_paragon_api_key(self, account_id: str, api_key: str):
        """Authenticate a Paragon API key.

        Args:
            account_id (str): The id of the account to authenticate.
            api_key (str): The API key to authenticate with.

        Returns:
            success: Whether the authentication was successful.
            error: The error message if authentication failed.
        """
        paragon_sk = self.get_paragon_api_key()
        if api_key != paragon_sk:
            return False, None, 'Invalid API Key'
        try:
            account = self.account_service.retrieve_by_id(account_id)
        except NotFoundError:
            return False, None, 'Invalid Account'
        return True, account, None

    def authenticate_account_token(self, account_id: str, token: str):
        """Authenticate an account using a JWT token.

        Args:
            account_id (str): The id of the account to authenticate.
            token (str): The JWT token to authenticate with.

        Returns:
            success: Whether the authentication was successful.
            account: The account document if authentication was successful.
            error: The error message if authentication failed.
        """
        user = self.get_user_by_token(token)
        if not user:
            return False, None, 'Invalid token'

        # Confirm the user has access to the requested account
        has_access = False
        for user_account in user.get('accounts', []):
            if user_account['id'] == account_id:
                has_access = True
                break
        if not has_access:
            return False, None, 'Access denied'

        return True, user, None

    def authenticate_user_token(self, token: str):
        """Authenticate a user using a JWT token.

        Args:
            token (str): The JWT token to authenticate with.

        Returns:
            success: Whether the authentication was successful.
            user: The user document if authentication was successful.
            error: The error message if authentication failed.
        """
        user = self.get_user_by_token(token)
        if not user:
            return False, None, 'Invalid token'
        return True, user, None
