# from app.api.deps import get_current_active_user
from app.crud import versify
from app.models.account import (
    Account,
    AccountCreate,
    AccountDeleteResult,
    AccountListResult,
    AccountUpdate,
)
from app.models.metadata import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/accounts", tags=["Accounts"])


# @router.get(
#     path="",
#     summary="List accounts",
#     description="List accounts with optional filters and pagination parameters",
#     status_code=status.HTTP_200_OK,
#     response_model=AccountListResult,
#     response_description="The list of accounts",
# )
# async def list_accounts(
#     user: User = Depends(get_current_active_user),
# ):
#     accounts = versify.list_accounts_by_email(email=user.email)
#     accounts_count = len(accounts)
#     return {'count': accounts_count, 'data': accounts, 'has_more': False}


# @router.post(
#     path="",
#     summary="Create an account",
#     description="Create an account",
#     status_code=status.HTTP_201_CREATED,
#     response_model=Account,
#     response_description="The created account",
# )
# async def create_account(
#     account_in: AccountCreate = BodyParams.CREATE_ACCOUNT,
#     user: User = Depends(get_current_active_user),
# ):
#     body = account_in.dict()
#     body["team"] = [{
#         "email": user.email,
#         "role": "admin",
#         "user": user.id
#     }]
#     created_account = versify.create_account(body)
#     return created_account


# @router.get(
#     path="/{account_id}",
#     summary="Get an account",
#     description="Get an account by ID",
#     status_code=status.HTTP_200_OK,
#     response_model=Account,
#     response_description="The account"
# )
# async def get_account(
#     account_id: str = PathParams.ACCOUNT_ID,
#     user: User = Depends(get_current_active_user),
# ):
#     account = versify.get_account_by_id(account_id)
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
#     return account


# @router.put(
#     path="/{account_id}",
#     summary="Update an account",
#     description="Update an account by ID",
#     status_code=status.HTTP_200_OK,
#     response_model=Account,
#     response_description="The updated account",
# )
# async def update_account(
#     account_id: str = PathParams.ACCOUNT_ID,
#     account_in: AccountUpdate = BodyParams.UPDATE_ACCOUNT,
#     user: User = Depends(get_current_active_user),
# ):
#     account = versify.get_account_by_id(account_id)
#     if not account:
#         raise HTTPException(status_code=404, detail="Account not found")
#     updated = versify.update_account(account_id, account_in.dict())
#     return updated or account


# @router.delete(
#     path="/{account_id}",
#     summary="Delete an account",
#     description="Delete an account by ID",
#     status_code=status.HTTP_200_OK,
#     response_model=AccountDeleteResult,
#     response_description="The deleted account",
# )
# async def delete_account(
#     # user: User = Depends(get_current_active_user),
#     account_id: str = PathParams.ACCOUNT_ID
# ):
#     deleted = versify.delete_account(account_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Account not found")
#     return AccountDeleteResult(id=account_id, deleted=deleted)
