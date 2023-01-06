from typing import Union

from app.api.exceptions import ForbiddenException
from app.api.models import HTTPAuthorizationCredentials, Identity
from app.api.security import HTTPBearer
from app.api.utils import get_current_user_account_role, get_user_from_credentials
from app.crud import versify
from app.models.enums import TeamMemberRole
from fastapi import Depends, Header

security = HTTPBearer(
    scheme_name="Access Token",
    description="Authorization header using the Bearer scheme.",
)


"""
Identity (run for every request)
"""


def identity(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Identity:
    """Get the identity from the request."""
    user = get_user_from_credentials(credentials)
    return Identity(user=user)


def identity_with_account(
    identity: Identity = Depends(identity),
    account_id: str = Header(
        default=None,
        alias="Versify-Account",
        description="Versify Account ID",
        title="Versify Account",
        example="act_123123123131231231",
    ),
) -> Identity:
    """Get the identity from the request."""
    user = identity.user
    account = versify.accounts.get(account_id)
    account_user_role = None
    if account:
        account_user_role = get_current_user_account_role(account, user)
    return Identity(
        user=user,
        account=account,
        account_user_role=account_user_role,
    )


"""
Guards (run for specific routes)
"""


def account_required(identity: Identity = Depends(identity)):
    """Require an account to be present in the identity."""
    if not identity.account:
        raise ForbiddenException("Account Required")


def account_role_required(
    identity: Identity = Depends(identity),
    role: TeamMemberRole = TeamMemberRole.ADMIN,
):
    """Require the user to have a specific role in the account."""
    if identity.account_user_role != role:
        raise ForbiddenException(f"{role.name} Required")


def user_required(identity: Identity = Depends(identity)):
    """Require a user to be present in the identity."""
    if not identity.user:
        raise ForbiddenException("User Required")
