from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.models.event import (
    EventCreateRequest,
    EventCreateResponse,
    EventDeleteResponse,
    EventGetResponse,
    EventListRequest,
    EventListResponse,
    EventSearchRequest,
    EventSearchResponse,
    EventUpdateRequest,
    EventUpdateResponse,
)
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/events", tags=["Events"])


@router.get(
    path="",
    summary="List events",
    description="List events with optional filters and pagination parameters",
    tags=["Events"],
    status_code=200,
    response_model=EventListResponse,
    response_description="The list of events",
)
def list_events(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    event_list_request: EventListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.events.count(
        account=current_account.id,
    )
    events = versify.events.list(
        page_num=event_list_request.page_num,
        page_size=event_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": events, "has_more": count > len(events)}


@router.post(
    path="/search",
    summary="Search events",
    description="Search events with query string",
    tags=["Events"],
    status_code=200,
    response_model=EventSearchResponse,
    response_description="The list of events",
)
def search_events(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    event_search_request: EventSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event_search_request_dict = event_search_request.dict()
    query = event_search_request_dict["query"]
    events = versify.events.search(account=current_account.id, query=query)
    return {"count": len(events), "data": events}


@router.post(
    path="",
    summary="Create event",
    description="Create a event",
    tags=["Events"],
    status_code=201,
    response_model=EventCreateResponse,
    response_description="The created event",
)
def create_event(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    event_create: EventCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = event_create.dict()
    body["account"] = current_account.id
    create_result = versify.events.create(body)
    return create_result


@router.get(
    path="/{event_id}",
    summary="Get event",
    description="Get a event",
    tags=["Events"],
    status_code=200,
    response_model=EventGetResponse,
    response_description="The event",
)
def get_event(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    event_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event = versify.events.get(event_id)
    if not event:
        raise NotFoundException()
    if event.account != current_account.id:
        raise ForbiddenException()
    return event


@router.put(
    path="/{event_id}",
    summary="Update event",
    description="Update an event",
    tags=["Events"],
    status_code=200,
    response_model=EventUpdateResponse,
    response_description="The updated event",
)
def update_event(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    event_id: str = PathParams.CONTACT_ID,
    event_update: EventUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event = versify.events.get(event_id)
    if not event:
        raise NotFoundException()
    if event.account != current_account.id:
        raise ForbiddenException()
    body = event_update.dict()
    update_result = versify.events.update(event_id, body)
    return update_result


@router.delete(
    path="/{event_id}",
    summary="Delete event",
    description="Delete an event",
    tags=["Events"],
    status_code=200,
    response_model=EventDeleteResponse,
    response_description="The deleted event",
)
def delete_event(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    event_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event = versify.events.get(event_id)
    if not event:
        raise NotFoundException()
    if event.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.events.delete(event_id)
    return delete_result
