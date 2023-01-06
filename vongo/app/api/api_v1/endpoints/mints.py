from fastapi import APIRouter, Depends

from ....crud import versify
from ....models.enums import TeamMemberRole
from ....models.mint import Mint, MintCreate, MintUpdate
from ...deps import identity_with_account
from ...exceptions import ForbiddenException, NotFoundException
from ...models import (
    ApiDeleteResponse,
    ApiListResponse,
    ApiSearchResponse,
    BodyParams,
    Identity,
    PathParams,
    QueryParams,
    SearchQuery,
)

router = APIRouter(prefix="/mints", tags=["Mints"])


@router.get(
    path="",
    summary="List mints",
    description="List mints with optional filters and pagination parameters",
    tags=["Mints"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of mints",
)
def list_mints(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.mints.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    mints = versify.mints.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": mints, "has_more": count > len(mints)}


@router.post(
    path="/search",
    summary="Search mints",
    description="Search mints with query string",
    tags=["Mints"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of mints",
)
def search_mints(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    mints = versify.mints.search(account=identity.account.id, query=query)
    return {"count": len(mints), "data": mints}


@router.post(
    path="",
    summary="Create mint",
    description="Create a mint",
    tags=["Mints"],
    status_code=201,
    response_model=Mint,
    response_description="The created mint",
)
def create_mint(
    identity: Identity = Depends(identity_with_account),
    mint_create: MintCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = mint_create.dict()
    body["account"] = identity.account.id
    create_result = versify.mints.create(body)
    return create_result


@router.get(
    path="/{mint_id}",
    summary="Get mint",
    description="Get a mint",
    tags=["Mints"],
    status_code=200,
    response_model=Mint,
    response_description="The mint",
)
def get_mint(
    identity: Identity = Depends(identity_with_account),
    mint_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint = versify.mints.get(mint_id)
    if not mint:
        raise NotFoundException("Mint not found")
    if mint.account != identity.account.id:
        raise ForbiddenException()
    return mint


@router.put(
    path="/{mint_id}",
    summary="Update mint",
    description="Update an mint",
    tags=["Mints"],
    status_code=200,
    response_model=Mint,
    response_description="The updated mint",
)
def update_mint(
    identity: Identity = Depends(identity_with_account),
    mint_id: str = PathParams.CONTACT_ID,
    mint_update: MintUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint = versify.mints.get(mint_id)
    if not mint:
        raise NotFoundException()
    if mint.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.mints.update(mint_id, mint_update.dict())
    return update_result


@router.delete(
    path="/{mint_id}",
    summary="Delete mint",
    description="Delete an mint",
    tags=["Mints"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted mint",
)
def delete_mint(
    identity: Identity = Depends(identity_with_account),
    mint_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint = versify.mints.get(mint_id)
    if not mint:
        raise NotFoundException()
    if mint.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.mints.delete(mint_id)
    return delete_result
