from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.models.exceptions import ForbiddenException, NotFoundException
from app.models.journey import (
    JourneyCreateRequest,
    JourneyCreateResponse,
    JourneyDeleteResponse,
    JourneyGetResponse,
    JourneyListRequest,
    JourneyListResponse,
    JourneySearchRequest,
    JourneySearchResponse,
    JourneyUpdateRequest,
    JourneyUpdateResponse,
)
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/journeys", tags=["Journeys"])


@router.get(
    path="",
    summary="List journeys",
    description="List journeys with optional filters and pagination parameters",
    tags=["Journeys"],
    status_code=200,
    response_model=JourneyListResponse,
    response_description="The list of journeys",
)
def list_journeys(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    journey_list_request: JourneyListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.journeys.count(
        account=current_account.id,
    )
    journeys = versify.journeys.list(
        page_num=journey_list_request.page_num,
        page_size=journey_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": journeys, "has_more": count > len(journeys)}


@router.post(
    path="/search",
    summary="Search journeys",
    description="Search journeys with query string",
    tags=["Journeys"],
    status_code=200,
    response_model=JourneySearchResponse,
    response_description="The list of journeys",
)
def search_journeys(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    journey_search_request: JourneySearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey_search_request_dict = journey_search_request.dict()
    query = journey_search_request_dict["query"]
    journeys = versify.journeys.search(account=current_account.id, query=query)
    return {"count": len(journeys), "data": journeys}


@router.post(
    path="",
    summary="Create journey",
    description="Create a journey",
    tags=["Journeys"],
    status_code=201,
    response_model=JourneyCreateResponse,
    response_description="The created journey",
)
def create_journey(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    journey_create: JourneyCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = journey_create.dict()
    body["account"] = current_account.id
    create_result = versify.journeys.create(body)
    return create_result


@router.get(
    path="/{journey_id}",
    summary="Get journey",
    description="Get a journey",
    tags=["Journeys"],
    status_code=200,
    response_model=JourneyGetResponse,
    response_description="The journey",
)
def get_journey(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    journey_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey = versify.journeys.get(journey_id)
    if not journey:
        raise NotFoundException()
    if journey.account != current_account.id:
        raise ForbiddenException()
    return journey


@router.put(
    path="/{journey_id}",
    summary="Update journey",
    description="Update an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=JourneyUpdateResponse,
    response_description="The updated journey",
)
def update_journey(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    journey_id: str = PathParams.CONTACT_ID,
    journey_update: JourneyUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey = versify.journeys.get(journey_id)
    if not journey:
        raise NotFoundException()
    if journey.account != current_account.id:
        raise ForbiddenException()
    body = journey_update.dict()
    update_result = versify.journeys.update(journey_id, body)
    return update_result


@router.delete(
    path="/{journey_id}",
    summary="Delete journey",
    description="Delete an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=JourneyDeleteResponse,
    response_description="The deleted journey",
)
def delete_journey(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    journey_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey = versify.journeys.get(journey_id)
    if not journey:
        raise
    if journey.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.journeys.delete(journey_id)
    return delete_result
