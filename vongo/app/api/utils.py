from ...exceptions import ForbiddenException, UnauthorizedException
from app.core.config import settings
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.models.user import User
from stytch.client import Client as StytchClient
from stytch.models.sessions import AuthenticateResponse as StytchAuthenticateResponse
from stytch.models.users import GetResponse as StytchGetResponse
from stytch.models.users import User as StytchUser

STYTCH_MAX_TOKEN_AGE_SECONDS = 3600000000

stytch_client = StytchClient(
    environment=settings.STYTCH_ENV,  # type: ignore
    project_id=settings.STYTCH_PROJECT_ID,  # type: ignore
    secret=settings.STYTCH_SECRET,  # type: ignore
    suppress_warnings=True,
)


def get_stytch_user(user_id) -> StytchGetResponse:
    """Get a Stytch user."""
    user = stytch_client.users.get(user_id)
    return user


def validate_stytch_token(session_jwt: str) -> StytchAuthenticateResponse:
    """Validate a Stytch token."""
    print(f"\nAccess Token:\n {session_jwt} \n")

    resp = stytch_client.sessions.authenticate_jwt(
        session_jwt, max_token_age_seconds=STYTCH_MAX_TOKEN_AGE_SECONDS
    )
    return resp


def convert_stytch_user(stytch_user: StytchUser) -> dict:
    """Convert a Stytch user to a Versify user."""

    user_body = {}
    if stytch_user.emails and len(stytch_user.emails) > 0:
        stytch_email = stytch_user.emails[0]
        user_body["email"] = stytch_email.email
        user_body["email_verified"] = stytch_email.verified
    if stytch_user.phone_numbers and len(stytch_user.phone_numbers) > 0:
        stytch_phone = stytch_user.phone_numbers[0]
        user_body["phone_number"] = stytch_phone.phone_number
        user_body["phone_number_verified"] = stytch_phone.verified
    if stytch_user.name:
        user_body["name"] = {
            "first_name": stytch_user.name.first_name,
            "middle_name": stytch_user.name.middle_name,
            "last_name": stytch_user.name.last_name,
        }
    user_body["providers"] = [
        {
            "provider_subject": stytch_user.user_id,
            "provider_type": "stytch",
        }
    ]
    for provider in stytch_user.providers:
        user_body["providers"].append(
            {
                "provider_subject": provider.provider_subject,
                "provider_type": provider.provider_type,
            }
        )
    # NOTE: We cannot use this because the URL changes
    # if stytch_user['providers'] and len(stytch_user['providers']) > 0:
    #     provider = stytch_user['providers'][0]
    #     user_body['avatar'] = provider.get('profile_picture_url')
    # for wallet in stytch_user.get('crypto_wallets', []):
    #     wallet_type = wallet.get('crypto_wallet_type')
    #     wallet_public_address = wallet.get('crypto_wallet_address')
    #     wallet_verifed = wallet.get('verified', False)
    return user_body


def get_user_from_credentials(credentials):
    """Get the user from the credentials."""

    resp = validate_stytch_token(credentials.token)
    if not resp or not resp.session:
        raise UnauthorizedException("Invalid Token")
    session = resp.session

    stytch_user_id = session.user_id
    stytch_user = get_stytch_user(stytch_user_id)
    user_body = convert_stytch_user(stytch_user)
    user = versify.users.get_by_email(user_body["email"])
    if not user:
        user = versify.users.create(user_body)
    if not user.active:
        raise ForbiddenException("User Inactive")

    return user


def get_current_user_account_role(account: Account, user: User):
    """Get the current user's role in the account."""

    for account_user in account.team:
        if account_user.email == user.email:
            return account_user.role

    return TeamMemberRole.GUEST
