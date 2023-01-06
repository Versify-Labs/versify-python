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
from app.crud import versify
from app.models.enums import TeamMemberRole
from app.models.journey import Journey, JourneyCreate, JourneyUpdate
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/journeys", tags=["Journeys"])


@router.get(
    path="",
    summary="List journeys",
    description="List journeys with optional filters and pagination parameters",
    tags=["Journeys"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of journeys",
)
def list_journeys(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.journeys.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    journeys = versify.journeys.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": journeys, "has_more": count > len(journeys)}


@router.post(
    path="/search",
    summary="Search journeys",
    description="Search journeys with query string",
    tags=["Journeys"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of journeys",
)
def search_journeys(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    journeys = versify.journeys.search(account=identity.account.id, query=query)
    return {"count": len(journeys), "data": journeys}


@router.post(
    path="",
    summary="Create journey",
    description="Create a journey",
    tags=["Journeys"],
    status_code=201,
    response_model=Journey,
    response_description="The created journey",
)
def create_journey(
    identity: Identity = Depends(identity_with_account),
    journey_create: JourneyCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = journey_create.dict()
    body["account"] = identity.account.id
    create_result = versify.journeys.create(body)
    return create_result


@router.get(
    path="/{journey_id}",
    summary="Get journey",
    description="Get a journey",
    tags=["Journeys"],
    status_code=200,
    response_model=Journey,
    response_description="The journey",
)
def get_journey(
    identity: Identity = Depends(identity_with_account),
    journey_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey = versify.journeys.get(journey_id)
    if not journey:
        raise NotFoundException("Journey not found")
    if journey.account != identity.account.id:
        raise ForbiddenException()
    return journey


@router.put(
    path="/{journey_id}",
    summary="Update journey",
    description="Update an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=Journey,
    response_description="The updated journey",
)
def update_journey(
    identity: Identity = Depends(identity_with_account),
    journey_id: str = PathParams.CONTACT_ID,
    journey_update: JourneyUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey = versify.journeys.get(journey_id)
    if not journey:
        raise NotFoundException()
    if journey.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.journeys.update(journey_id, journey_update.dict())
    return update_result


@router.delete(
    path="/{journey_id}",
    summary="Delete journey",
    description="Delete an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted journey",
)
def delete_journey(
    identity: Identity = Depends(identity_with_account),
    journey_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    journey = versify.journeys.get(journey_id)
    if not journey:
        raise NotFoundException()
    if journey.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.journeys.delete(journey_id)
    return delete_result
