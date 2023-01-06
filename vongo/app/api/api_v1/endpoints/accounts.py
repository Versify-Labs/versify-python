from typing import List, Union

from app.api.deps import get_current_user_account_role, identity, user_required
from app.api.exceptions import ForbiddenException, NotFoundException
from app.api.models import (
    ApiDeleteResponse,
    ApiListResponse,
    BodyParams,
    Identity,
    PathParams,
    QueryParams,
)
from app.crud import versify
from app.models.account import Account, AccountCreate, AccountUpdate
from app.models.enums import TeamMemberRole
from app.models.globals import AccountMetrics
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get(
    path="",
    summary="List accounts",
    description="List accounts with optional filters and pagination parameters",
    status_code=status.HTTP_200_OK,
    response_model=ApiListResponse,
    response_description="The list of accounts",
    dependencies=[Depends(user_required)],
)
async def list_accounts(
    identity: Identity = Depends(identity),
):
    accounts = versify.accounts.list_by_email(identity.user.email)  # type: ignore
    accounts_count = len(accounts)
    return {"count": accounts_count, "data": accounts, "has_more": False}


@router.post(
    path="",
    summary="Create an account",
    description="Create an account",
    status_code=status.HTTP_201_CREATED,
    response_model=Account,
    response_description="The created account",
    dependencies=[Depends(user_required)],
)
async def create_account(
    identity: Identity = Depends(identity),
    account_create: AccountCreate = BodyParams.CREATE_ACCOUNT,
):
    body = account_create.dict()
    body["team"] = [
        {
            "email": identity.user.email,  # type: ignore
            "role": TeamMemberRole.ADMIN,
            "user": identity.user.id,  # type: ignore
        }
    ]
    created_account = versify.accounts.create(body)
    return created_account


@router.get(
    path="/{account_id}",
    summary="Get an account",
    description="Get an account by ID",
    status_code=status.HTTP_200_OK,
    response_model=Account,
    response_description="The account",
    dependencies=[Depends(user_required)],
)
async def get_account(
    identity: Identity = Depends(identity),
    account_id: str = PathParams.ACCOUNT_ID,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise NotFoundException("Account not found")
    account_role = get_current_user_account_role(account, identity.user)  # type: ignore
    if account_role == TeamMemberRole.ADMIN:
        return account
    elif account_role == TeamMemberRole.MEMBER:
        return account
    else:
        raise ForbiddenException("You do not have access to this account")


@router.put(
    path="/{account_id}",
    summary="Update an account",
    description="Update an account by ID",
    status_code=status.HTTP_200_OK,
    response_model=Account,
    response_description="The updated account",
    dependencies=[Depends(user_required)],
)
async def update_account(
    identity: Identity = Depends(identity),
    account_id: str = PathParams.ACCOUNT_ID,
    account_update: AccountUpdate = BodyParams.UPDATE_ACCOUNT,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise NotFoundException("Account not found")
    account_role = get_current_user_account_role(account, identity.user)  # type: ignore
    if account_role == TeamMemberRole.ADMIN:
        updated = versify.accounts.update(account_id, account_update.dict())
        return updated
    elif account_role == TeamMemberRole.MEMBER:
        updated = versify.accounts.update(account_id, account_update.dict())
        return updated
    else:
        raise ForbiddenException("You do not have access to this account")


@router.delete(
    path="/{account_id}",
    summary="Delete an account",
    description="Delete an account by ID",
    status_code=status.HTTP_200_OK,
    response_model=ApiDeleteResponse,
    response_description="The deleted account",
    dependencies=[Depends(user_required)],
)
async def delete_account(
    identity: Identity = Depends(identity),
    account_id: str = PathParams.ACCOUNT_ID,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise NotFoundException("Account not found")
    account_role = get_current_user_account_role(account, identity.user)  # type: ignore
    if account_role == TeamMemberRole.ADMIN:
        deleted = versify.accounts.delete(account_id)
        return {"id": account_id, object: "account", "deleted": deleted}
    else:
        raise ForbiddenException("You do not have access to this account")


@router.get(
    path="/{account_id}/metrics",
    summary="Get account metrics",
    description="Get account metrics by ID",
    status_code=status.HTTP_200_OK,
    response_model=AccountMetrics,
    response_description="The account",
    dependencies=[Depends(user_required)],
)
async def get_account_metrics(
    identity: Identity = Depends(identity),
    account_id: str = PathParams.ACCOUNT_ID,
    object_types: Union[List[str], None] = QueryParams.OBJECT_TYPES,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise NotFoundException("Account not found")
    account_role = get_current_user_account_role(account, identity.user)  # type: ignore
    if account_role == TeamMemberRole.ADMIN:
        return versify.accounts.get_metrics(account_id, object_types)
    elif account_role == TeamMemberRole.MEMBER:
        return versify.accounts.get_metrics(account_id, object_types)
    else:
        raise ForbiddenException("You do not have access to this account")
