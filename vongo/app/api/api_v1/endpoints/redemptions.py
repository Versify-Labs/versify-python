from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.models.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.redemption import (
    RedemptionCreateRequest,
    RedemptionCreateResponse,
    RedemptionDeleteResponse,
    RedemptionGetResponse,
    RedemptionListRequest,
    RedemptionListResponse,
    RedemptionSearchRequest,
    RedemptionSearchResponse,
    RedemptionUpdateRequest,
    RedemptionUpdateResponse,
)
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/redemptions", tags=["Redemptions"])


@router.get(
    path="",
    summary="List redemptions",
    description="List redemptions with optional filters and pagination parameters",
    tags=["Redemptions"],
    status_code=200,
    response_model=RedemptionListResponse,
    response_description="The list of redemptions",
)
def list_redemptions(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    redemption_list_request: RedemptionListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.redemptions.count(
        account=current_account.id,
    )
    redemptions = versify.redemptions.list(
        page_num=redemption_list_request.page_num,
        page_size=redemption_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": redemptions, "has_more": count > len(redemptions)}


@router.post(
    path="/search",
    summary="Search redemptions",
    description="Search redemptions with query string",
    tags=["Redemptions"],
    status_code=200,
    response_model=RedemptionSearchResponse,
    response_description="The list of redemptions",
)
def search_redemptions(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    redemption_search_request: RedemptionSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption_search_request_dict = redemption_search_request.dict()
    query = redemption_search_request_dict["query"]
    redemptions = versify.redemptions.search(account=current_account.id, query=query)
    return {"count": len(redemptions), "data": redemptions}


@router.post(
    path="",
    summary="Create redemption",
    description="Create a redemption",
    tags=["Redemptions"],
    status_code=201,
    response_model=RedemptionCreateResponse,
    response_description="The created redemption",
)
def create_redemption(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    redemption_create: RedemptionCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = redemption_create.dict()
    body["account"] = current_account.id
    create_result = versify.redemptions.create(body)
    return create_result


@router.get(
    path="/{redemption_id}",
    summary="Get redemption",
    description="Get a redemption",
    tags=["Redemptions"],
    status_code=200,
    response_model=RedemptionGetResponse,
    response_description="The redemption",
)
def get_redemption(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    redemption_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption = versify.redemptions.get(redemption_id)
    if not redemption:
        raise NotFoundException()
    if redemption.account != current_account.id:
        raise ForbiddenException()
    return redemption


@router.put(
    path="/{redemption_id}",
    summary="Update redemption",
    description="Update an redemption",
    tags=["Redemptions"],
    status_code=200,
    response_model=RedemptionUpdateResponse,
    response_description="The updated redemption",
)
def update_redemption(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    redemption_id: str = PathParams.CONTACT_ID,
    redemption_update: RedemptionUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption = versify.redemptions.get(redemption_id)
    if not redemption:
        raise NotFoundException()
    if redemption.account != current_account.id:
        raise ForbiddenException()
    body = redemption_update.dict()
    update_result = versify.redemptions.update(redemption_id, body)
    return update_result


@router.delete(
    path="/{redemption_id}",
    summary="Delete redemption",
    description="Delete an redemption",
    tags=["Redemptions"],
    status_code=200,
    response_model=RedemptionDeleteResponse,
    response_description="The deleted redemption",
)
def delete_redemption(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    redemption_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption = versify.redemptions.get(redemption_id)
    if not redemption:
        raise NotFoundException()
    if redemption.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.redemptions.delete(redemption_id)
    return delete_result
