from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.asset import (
    AssetCreateRequest,
    AssetCreateResponse,
    AssetDeleteRequest,
    AssetDeleteResponse,
    AssetGetRequest,
    AssetGetResponse,
    AssetListRequest,
    AssetListResponse,
    AssetSearchRequest,
    AssetSearchResponse,
    AssetUpdateRequest,
    AssetUpdateResponse,
)
from app.models.enums import TeamMemberRole
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get(
    path="",
    summary="List assets",
    description="List assets with optional filters and pagination parameters",
    tags=["Assets"],
    status_code=200,
    response_model=AssetListResponse,
    response_description="The list of assets",
)
def list_assets(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    asset_list_request: AssetListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to list assets.",
        )
    count = versify.assets.count(
        account=current_account.id,
        collection=asset_list_request.collection,
        status=asset_list_request.status,
        tags=asset_list_request.tags,
    )
    assets = versify.assets.list(
        page_num=asset_list_request.page_num,
        page_size=asset_list_request.page_size,
        account=current_account.id,
        collection=asset_list_request.collection,
        status=asset_list_request.status,
        tags=asset_list_request.tags,
    )
    return {"count": count, "data": assets, "has_more": count > len(assets)}


@router.post(
    path="/search",
    summary="Search assets",
    description="Search assets with query string",
    tags=["Assets"],
    status_code=200,
    response_model=AssetSearchResponse,
    response_description="The list of assets",
)
def search_assets(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    asset_search_request: AssetSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to search assets.",
        )
    asset_search_request_dict = asset_search_request.dict()
    query = asset_search_request_dict["query"]
    assets = versify.assets.search(account=current_account.id, query=query)
    return {"count": len(assets), "data": assets}


@router.post(
    path="",
    summary="Create asset",
    description="Create a asset",
    tags=["Assets"],
    status_code=201,
    response_model=AssetCreateResponse,
    response_description="The created asset",
)
def create_asset(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    asset_create: AssetCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create assets.",
        )
    body = asset_create.dict()
    body["account"] = current_account.id
    create_result = versify.assets.create(body)
    return create_result


@router.get(
    path="/{asset_id}",
    summary="Get asset",
    description="Get a asset",
    tags=["Assets"],
    status_code=200,
    response_model=AssetGetResponse,
    response_description="The asset",
)
def get_asset(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    asset_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view assets.",
        )
    asset = versify.assets.get(asset_id)
    if not asset:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if asset.account != current_account.id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view assets for this account.",
        )
    return asset


@router.put(
    path="/{asset_id}",
    summary="Update asset",
    description="Update an asset",
    tags=["Assets"],
    status_code=200,
    response_model=AssetUpdateResponse,
    response_description="The updated asset",
)
def update_asset(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    asset_id: str = PathParams.CONTACT_ID,
    asset_update: AssetUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update assets.",
        )
    asset = versify.assets.get(asset_id)
    if not asset:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if asset.account != current_account.id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update assets for this account.",
        )
    body = asset_update.dict()
    update_result = versify.assets.update(asset_id, body)
    return update_result


@router.delete(
    path="/{asset_id}",
    summary="Delete asset",
    description="Delete an asset",
    tags=["Assets"],
    status_code=200,
    response_model=AssetDeleteResponse,
    response_description="The deleted asset",
)
def delete_asset(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    asset_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete assets.",
        )
    asset = versify.assets.get(asset_id)
    if not asset:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if asset.account != current_account.id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete assets for this account.",
        )
    delete_result = versify.assets.delete(asset_id)
    return delete_result
