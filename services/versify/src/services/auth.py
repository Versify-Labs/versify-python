"""Can authenticate an API call with a token and account id."""
from aws_lambda_powertools import Logger, Tracer
from jose import jwt

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

    def get_user_by_token(self, token: str):
        """Get a user by token.

        Args:
            token (str): The token to retrieve.

        Returns:
            dict: The user.
        """
        if not token:
            return

        claims = jwt.get_unverified_claims(token)
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
                user_body['wallets'] = user['crypto_wallets']

        return self.user_service.login(user_body)

    def authenticate_account_api_key(self, api_key: str):
        """Authenticate an account using an API key.

        Args:
            api_key (str): The API key to authenticate with.

        Returns:
            success: Whether the authentication was successful.
            account: The account document if authentication was successful.
            error: The error message if authentication failed.
        """
        account = self.account_service.retrieve_by_api_secret_key(api_key)
        if not account:
            return False, None, 'Invalid API key'
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
