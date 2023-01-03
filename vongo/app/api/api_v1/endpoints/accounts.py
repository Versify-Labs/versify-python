from app.api.deps import current_active_user, get_current_user_account_role
from app.crud import versify
from app.models.account import (
    Account,
    AccountCreateRequest,
    AccountDeleteResponse,
    AccountListResponse,
    AccountUpdateRequest,
)
from app.models.enums import TeamMemberRole
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get(
    path="",
    summary="List accounts",
    description="List accounts with optional filters and pagination parameters",
    status_code=status.HTTP_200_OK,
    response_model=AccountListResponse,
    response_description="The list of accounts",
)
async def list_accounts(
    current_user: User = Depends(current_active_user),
):
    accounts = versify.accounts.list_by_email(email=current_user.email)
    accounts_count = len(accounts)
    return {"count": accounts_count, "data": accounts, "has_more": False}


@router.post(
    path="",
    summary="Create an account",
    description="Create an account",
    status_code=status.HTTP_201_CREATED,
    response_model=Account,
    response_description="The created account",
)
async def create_account(
    current_user: User = Depends(current_active_user),
    account_create: AccountCreateRequest = BodyParams.CREATE_ACCOUNT,
):
    body = account_create.dict()
    body["team"] = [
        {
            "email": current_user.email,
            "role": TeamMemberRole.ADMIN,
            "user": current_user.id,
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
)
async def get_account(
    current_user: User = Depends(current_active_user),
    account_id: str = PathParams.ACCOUNT_ID,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    role = get_current_user_account_role(account, current_user)
    if role == TeamMemberRole.ADMIN or role == TeamMemberRole.MEMBER:
        return account
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.put(
    path="/{account_id}",
    summary="Update an account",
    description="Update an account by ID",
    status_code=status.HTTP_200_OK,
    response_model=Account,
    response_description="The updated account",
)
async def update_account(
    current_user: User = Depends(current_active_user),
    account_id: str = PathParams.ACCOUNT_ID,
    account_update: AccountUpdateRequest = BodyParams.UPDATE_ACCOUNT,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    role = get_current_user_account_role(account, current_user)
    if role == TeamMemberRole.ADMIN:
        updated = versify.accounts.update(account_id, account_update.dict())
        return updated or account
    elif role == TeamMemberRole.MEMBER:
        updated = versify.accounts.update(account_id, account_update.dict())
        return updated or account
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.delete(
    path="/{account_id}",
    summary="Delete an account",
    description="Delete an account by ID",
    status_code=status.HTTP_200_OK,
    response_model=AccountDeleteResponse,
    response_description="The deleted account",
)
async def delete_account(
    current_user: User = Depends(current_active_user),
    account_id: str = PathParams.ACCOUNT_ID,
):
    account = versify.accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    role = get_current_user_account_role(account, current_user)
    if role == TeamMemberRole.ADMIN:
        deleted = versify.accounts.delete(account_id)
        return AccountDeleteResponse(id=account_id, deleted=deleted)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
