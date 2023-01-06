from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.mint import (
    MintCreateRequest,
    MintCreateResponse,
    MintDeleteResponse,
    MintGetResponse,
    MintListRequest,
    MintListResponse,
    MintSearchRequest,
    MintSearchResponse,
    MintUpdateRequest,
    MintUpdateResponse,
)
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/mints", tags=["Mints"])


@router.get(
    path="",
    summary="List mints",
    description="List mints with optional filters and pagination parameters",
    tags=["Mints"],
    status_code=200,
    response_model=MintListResponse,
    response_description="The list of mints",
)
def list_mints(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    mint_list_request: MintListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.mints.count(
        account=current_account.id,
    )
    mints = versify.mints.list(
        page_num=mint_list_request.page_num,
        page_size=mint_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": mints, "has_more": count > len(mints)}


@router.post(
    path="/search",
    summary="Search mints",
    description="Search mints with query string",
    tags=["Mints"],
    status_code=200,
    response_model=MintSearchResponse,
    response_description="The list of mints",
)
def search_mints(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    mint_search_request: MintSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint_search_request_dict = mint_search_request.dict()
    query = mint_search_request_dict["query"]
    mints = versify.mints.search(account=current_account.id, query=query)
    return {"count": len(mints), "data": mints}


@router.post(
    path="",
    summary="Create mint",
    description="Create a mint",
    tags=["Mints"],
    status_code=201,
    response_model=MintCreateResponse,
    response_description="The created mint",
)
def create_mint(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    mint_create: MintCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = mint_create.dict()
    body["account"] = current_account.id
    create_result = versify.mints.create(body)
    return create_result


@router.get(
    path="/{mint_id}",
    summary="Get mint",
    description="Get a mint",
    tags=["Mints"],
    status_code=200,
    response_model=MintGetResponse,
    response_description="The mint",
)
def get_mint(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    mint_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint = versify.mints.get(mint_id)
    if not mint:
        raise NotFoundException()
    if mint.account != current_account.id:
        raise ForbiddenException()
    return mint


@router.put(
    path="/{mint_id}",
    summary="Update mint",
    description="Update an mint",
    tags=["Mints"],
    status_code=200,
    response_model=MintUpdateResponse,
    response_description="The updated mint",
)
def update_mint(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    mint_id: str = PathParams.CONTACT_ID,
    mint_update: MintUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint = versify.mints.get(mint_id)
    if not mint:
        raise NotFoundException()
    if mint.account != current_account.id:
        raise ForbiddenException()
    body = mint_update.dict()
    update_result = versify.mints.update(mint_id, body)
    return update_result


@router.delete(
    path="/{mint_id}",
    summary="Delete mint",
    description="Delete an mint",
    tags=["Mints"],
    status_code=200,
    response_model=MintDeleteResponse,
    response_description="The deleted mint",
)
def delete_mint(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    mint_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    mint = versify.mints.get(mint_id)
    if not mint:
        raise NotFoundException()
    if mint.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.mints.delete(mint_id)
    return delete_result
