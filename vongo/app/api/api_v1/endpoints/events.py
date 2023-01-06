from fastapi import APIRouter, Depends

from ....crud import versify
from ....models.enums import TeamMemberRole
from ....models.event import Event, EventCreate, EventUpdate
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

router = APIRouter(prefix="/events", tags=["Events"])


@router.get(
    path="",
    summary="List events",
    description="List events with optional filters and pagination parameters",
    tags=["Events"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of events",
)
def list_events(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    event: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.events.count(
        account=identity.account.id,  # type: ignore
        event=event,
        status=status,
    )
    events = versify.events.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        event=event,
        status=status,
    )
    return {"count": count, "data": events, "has_more": count > len(events)}


@router.post(
    path="/search",
    summary="Search events",
    description="Search events with query string",
    tags=["Events"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of events",
)
def search_events(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    events = versify.events.search(account=identity.account.id, query=query)
    return {"count": len(events), "data": events}


@router.post(
    path="",
    summary="Create event",
    description="Create a event",
    tags=["Events"],
    status_code=201,
    response_model=Event,
    response_description="The created event",
)
def create_event(
    identity: Identity = Depends(identity_with_account),
    event_create: EventCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = event_create.dict()
    body["account"] = identity.account.id
    create_result = versify.events.create(body)
    return create_result


@router.get(
    path="/{event_id}",
    summary="Get event",
    description="Get a event",
    tags=["Events"],
    status_code=200,
    response_model=Event,
    response_description="The event",
)
def get_event(
    identity: Identity = Depends(identity_with_account),
    event_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event = versify.events.get(event_id)
    if not event:
        raise NotFoundException("Event not found")
    if event.account != identity.account.id:
        raise ForbiddenException()
    return event


@router.put(
    path="/{event_id}",
    summary="Update event",
    description="Update an event",
    tags=["Events"],
    status_code=200,
    response_model=Event,
    response_description="The updated event",
)
def update_event(
    identity: Identity = Depends(identity_with_account),
    event_id: str = PathParams.CONTACT_ID,
    event_update: EventUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event = versify.events.get(event_id)
    if not event:
        raise NotFoundException()
    if event.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.events.update(event_id, event_update.dict())
    return update_result


@router.delete(
    path="/{event_id}",
    summary="Delete event",
    description="Delete an event",
    tags=["Events"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted event",
)
def delete_event(
    identity: Identity = Depends(identity_with_account),
    event_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    event = versify.events.get(event_id)
    if not event:
        raise NotFoundException()
    if event.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.events.delete(event_id)
    return delete_result
