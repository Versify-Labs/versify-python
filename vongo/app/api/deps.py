import stytch
from app.core.config import settings
from app.crud import versify
from app.models.user import User
from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt


def get_stytch_user(stytch_user_id: str):
    stytch_client = stytch.Client(
        project_id=settings.STYTCH_PROJECT_ID,  # type: ignore
        secret=settings.STYTCH_SECRET,  # type: ignore
        environment=settings.STYTCH_ENV,  # type: ignore
    )
    stytch_user_response = stytch_client.users.get(stytch_user_id)
    stytch_user = stytch_user_response.json()
    return stytch_user


def convert_stytch_user(stytch_user):
    user_body = {}
    if stytch_user['emails'] and len(stytch_user['emails']) > 0:
        user_body['email'] = stytch_user['emails'][0]['email']
        user_body['email_verified'] = stytch_user['emails'][0]['verified']
    if stytch_user['phone_numbers'] and len(stytch_user['phone_numbers']) > 0:
        user_body['phone_number'] = stytch_user['phone_numbers'][0]['phone_number']
        user_body['phone_number_verified'] = stytch_user['phone_numbers'][0]['verified']
    if stytch_user['name']:
        user_body['name'] = {
            'first_name': stytch_user['name'].get('first_name'),
            'middle_name': stytch_user['name'].get('middle_name'),
            'last_name': stytch_user['name'].get('last_name')
        }
    user_body['providers'] = [{
        'provider_subject': stytch_user['user_id'],
        'provider_type': 'stytch',
    }]
    for provider in stytch_user.get('providers', []):
        user_body['providers'].append({
            'provider_subject': provider.get('provider_subject', '').lower(),
            'provider_type': provider.get('provider_type', '').lower(),
        })
    # NOTE: We cannot use this because the URL changes
    # if stytch_user['providers'] and len(stytch_user['providers']) > 0:
    #     provider = stytch_user['providers'][0]
    #     user_body['avatar'] = provider.get('profile_picture_url')
    # for wallet in stytch_user.get('crypto_wallets', []):
    #     wallet_type = wallet.get('crypto_wallet_type')
    #     wallet_public_address = wallet.get('crypto_wallet_address')
    #     wallet_verifed = wallet.get('verified', False)
    return user_body


def get_user_body_from_stytch(stytch_user_id: str):
    if not stytch_user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid Stytch User ID"
        )
    stytch_user = get_stytch_user(stytch_user_id)
    versify_user = convert_stytch_user(stytch_user)
    return versify_user


def get_user_body_from_stytch_claims(claims):

    session = claims.get('https://stytch.com/session')
    stytch_user_id = claims.get('sub')
    if not session or not stytch_user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid Token. Missing Stytch User ID or Session"
        )

    user_body = {}
    for factor in session.get('authentication_factors', []):
        if factor.get('type') == 'oauth':
            stytch_user = get_stytch_user(stytch_user_id)
            user_body = convert_stytch_user(stytch_user)
        elif factor.get('type') in ['magic_link', 'otp']:
            email_factor = factor.get('email_factor', {})
            email = email_factor.get('email_address')
            user_body['email'] = email
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid Authentication Factor"
            )
        break

    return user_body


async def get_current_user(
    authorization: str = Header(None, alias="Authorization")
):

    # Verify the authorization header is present and valid
    if not authorization:
        raise HTTPException(
            status_code=400,
            detail="Authorization Header Missing"
        )
    auth_type, token = authorization.split(" ")
    if not auth_type or not token:
        raise HTTPException(
            status_code=400,
            detail="Authorization Header Malformed"
        )
    if auth_type.lower() != "bearer":
        raise HTTPException(
            status_code=400,
            detail="Authorization Type Not Supported"
        )

    # Verify the token is valid
    try:
        claims = jwt.get_unverified_claims(token)
    except JWTError:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Invalid Token"
        )
    if not claims:
        raise HTTPException(
            status_code=400,
            detail="Invalid Token"
        )

    user_body = get_user_body_from_stytch_claims(claims)
    if not user_body.get('email'):
        raise HTTPException(
            status_code=400,
            detail="Could not identify user email address"
        )

    user = versify.get_user_by_email(user_body['email'])
    if not user:
        user = versify.create_user(user_body)

    return user


async def get_current_active_user(
    user: User = Depends(get_current_user),
):
    if not user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# async def get_current_active_account_member(
#     user: User = Depends(get_current_active_user),
#     account_id: str = metadata.PathParams.ACCOUNT_ID,
# ):
#     if not user.active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     role = None
#     user_accounts = versify.list_accounts_by_email(user.email)
#     for account in user_accounts:
#         if account.id == account_id:
#             for teammate in account.team:
#                 if teammate.email == user.email:
#                     role = teammate.role
#     if not role:
#         raise HTTPException(status_code=403, detail="Forbidden")
#     return user


# async def get_current_active_account_admin(
#     user: User = Depends(get_current_active_user),
#     account_id: str = metadata.PathParams.ACCOUNT_ID,
# ):
#     if not user.active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     role = None
#     user_accounts = versify.list_accounts_by_email(user.email)
#     for account in user_accounts:
#         if account.id == account_id:
#             for teammate in account.team:
#                 if teammate.email == user.email:
#                     role = teammate.role
#     if not role:
#         raise HTTPException(status_code=403, detail="Forbidden")
#     return role == 'admin'
