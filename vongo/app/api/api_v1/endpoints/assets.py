from app.api.deps import identity_with_account
from app.api.exceptions import ForbiddenException, NotFoundException
from app.api.models import (
    ApiDeleteResponse,
    ApiListResponse,
    ApiSearchResponse,
    BodyParams,
    Identity,
    PathParams,
    QueryParams,
    SearchQuery,
)
from app.crud import versify
from app.models.asset import Asset, AssetCreate, AssetUpdate
from app.models.enums import TeamMemberRole
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get(
    path="",
    summary="List assets",
    description="List assets with optional filters and pagination parameters",
    tags=["Assets"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of assets",
)
def list_assets(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.assets.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    assets = versify.assets.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": assets, "has_more": count > len(assets)}


@router.post(
    path="/search",
    summary="Search assets",
    description="Search assets with query string",
    tags=["Assets"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of assets",
)
def search_assets(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    assets = versify.assets.search(account=identity.account.id, query=query)
    return {"count": len(assets), "data": assets}


@router.post(
    path="",
    summary="Create asset",
    description="Create a asset",
    tags=["Assets"],
    status_code=201,
    response_model=Asset,
    response_description="The created asset",
)
def create_asset(
    identity: Identity = Depends(identity_with_account),
    asset_create: AssetCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = asset_create.dict()
    body["account"] = identity.account.id
    create_result = versify.assets.create(body)
    return create_result


@router.get(
    path="/{asset_id}",
    summary="Get asset",
    description="Get a asset",
    tags=["Assets"],
    status_code=200,
    response_model=Asset,
    response_description="The asset",
)
def get_asset(
    identity: Identity = Depends(identity_with_account),
    asset_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    asset = versify.assets.get(asset_id)
    if not asset:
        raise NotFoundException("Asset not found")
    if asset.account != identity.account.id:
        raise ForbiddenException()
    return asset


@router.put(
    path="/{asset_id}",
    summary="Update asset",
    description="Update an asset",
    tags=["Assets"],
    status_code=200,
    response_model=Asset,
    response_description="The updated asset",
)
def update_asset(
    identity: Identity = Depends(identity_with_account),
    asset_id: str = PathParams.CONTACT_ID,
    asset_update: AssetUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    asset = versify.assets.get(asset_id)
    if not asset:
        raise NotFoundException()
    if asset.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.assets.update(asset_id, asset_update.dict())
    return update_result


@router.delete(
    path="/{asset_id}",
    summary="Delete asset",
    description="Delete an asset",
    tags=["Assets"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted asset",
)
def delete_asset(
    identity: Identity = Depends(identity_with_account),
    asset_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    asset = versify.assets.get(asset_id)
    if not asset:
        raise NotFoundException()
    if asset.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.assets.delete(asset_id)
    return delete_result
