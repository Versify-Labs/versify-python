from app.api.exceptions import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from app.core.stytch import load_stytch
from app.crud import versify
from app.models.account import Account
from app.models.enums import AccountStatus, TeamMemberRole
from app.models.params import HeaderParams
from app.models.user import User
from fastapi import Depends
from jose import JWTError, jwt

stytch = load_stytch()


def convert_stytch_user(stytch_user):
    user_body = {}
    if stytch_user["emails"] and len(stytch_user["emails"]) > 0:
        user_body["email"] = stytch_user["emails"][0]["email"]
        user_body["email_verified"] = stytch_user["emails"][0]["verified"]
    if stytch_user["phone_numbers"] and len(stytch_user["phone_numbers"]) > 0:
        user_body["phone_number"] = stytch_user["phone_numbers"][0]["phone_number"]
        user_body["phone_number_verified"] = stytch_user["phone_numbers"][0]["verified"]
    if stytch_user["name"]:
        user_body["name"] = {
            "first_name": stytch_user["name"].get("first_name"),
            "middle_name": stytch_user["name"].get("middle_name"),
            "last_name": stytch_user["name"].get("last_name"),
        }
    user_body["providers"] = [
        {
            "provider_subject": stytch_user["user_id"],
            "provider_type": "stytch",
        }
    ]
    for provider in stytch_user.get("providers", []):
        user_body["providers"].append(
            {
                "provider_subject": provider.get("provider_subject", "").lower(),
                "provider_type": provider.get("provider_type", "").lower(),
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


def get_user_body_from_stytch_claims(claims):

    session = claims.get("https://stytch.com/session")
    stytch_user_id = claims.get("sub")
    if not session or not stytch_user_id:
        raise UnauthorizedException("Invalid Token")

    user_body = {}
    for factor in session.get("authentication_factors", []):
        if factor.get("type") == "oauth":
            stytch_user = stytch.get_user(stytch_user_id)
            user_body = convert_stytch_user(stytch_user)
        elif factor.get("type") in ["magic_link", "otp"]:
            email_factor = factor.get("email_factor", {})
            email = email_factor.get("email_address")
            user_body["email"] = email
        else:
            raise UnauthorizedException("Invalid Token")
        break

    return user_body


def current_user(authorization: str = HeaderParams.AUTHORIZATION):

    if not authorization:
        raise UnauthorizedException("Missing Authorization Header")
    auth_type, token = authorization.split(" ")
    if not auth_type or not token:
        raise UnauthorizedException("Invalid Authorization Header")
    if auth_type.lower() != "bearer":
        raise UnauthorizedException("Invalid Authorization Header")

    try:
        claims = jwt.get_unverified_claims(token)
    except JWTError:
        raise UnauthorizedException("Invalid Token")
    if not claims:
        raise UnauthorizedException("Invalid Token")

    user_body = get_user_body_from_stytch_claims(claims)
    if not user_body.get("email"):
        raise UnauthorizedException("Invalid Token")

    user = versify.users.get_by_email(user_body["email"])
    if not user:
        user = versify.users.create(user_body)

    return user


def current_active_user(user: User = Depends(current_user)):
    if not user.active:
        raise ForbiddenException("User Inactive")
    return user


def current_account(account_id: str = HeaderParams.VERSIFY_ACCOUNT):
    if not account_id:
        raise NotFoundException("Account Not Found")
    account = versify.accounts.get_by_id(account_id)
    if not account:
        raise NotFoundException("Account Not Found")
    return account


def current_active_account(account: Account = Depends(current_account)):
    if not account.status == AccountStatus.ACTIVE:
        raise ForbiddenException("Account Inactive")
    return account


def get_current_user_account_role(account: Account, user: User):
    for account_user in account.team:
        if account_user.email == user.email:
            return account_user.role
    return TeamMemberRole.GUEST


def current_user_account_role(
    account: Account = Depends(current_active_account),
    user: User = Depends(current_active_user),
) -> TeamMemberRole:
    return get_current_user_account_role(account, user)
