from app.api.deps import identity_with_account
from app.crud import versify
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
from app.models.redemption import Redemption, RedemptionCreate, RedemptionUpdate

from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/redemptions", tags=["Redemptions"])


@router.get(
    path="",
    summary="List redemptions",
    description="List redemptions with optional filters and pagination parameters",
    tags=["Redemptions"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of redemptions",
)
def list_redemptions(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.redemptions.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    redemptions = versify.redemptions.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": redemptions, "has_more": count > len(redemptions)}


@router.post(
    path="/search",
    summary="Search redemptions",
    description="Search redemptions with query string",
    tags=["Redemptions"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of redemptions",
)
def search_redemptions(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    redemptions = versify.redemptions.search(account=identity.account.id, query=query)
    return {"count": len(redemptions), "data": redemptions}


@router.post(
    path="",
    summary="Create redemption",
    description="Create a redemption",
    tags=["Redemptions"],
    status_code=201,
    response_model=Redemption,
    response_description="The created redemption",
)
def create_redemption(
    identity: Identity = Depends(identity_with_account),
    redemption_create: RedemptionCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = redemption_create.dict()
    body["account"] = identity.account.id
    create_result = versify.redemptions.create(body)
    return create_result


@router.get(
    path="/{redemption_id}",
    summary="Get redemption",
    description="Get a redemption",
    tags=["Redemptions"],
    status_code=200,
    response_model=Redemption,
    response_description="The redemption",
)
def get_redemption(
    identity: Identity = Depends(identity_with_account),
    redemption_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption = versify.redemptions.get(redemption_id)
    if not redemption:
        raise NotFoundException("Redemption not found")
    if redemption.account != identity.account.id:
        raise ForbiddenException()
    return redemption


@router.put(
    path="/{redemption_id}",
    summary="Update redemption",
    description="Update an redemption",
    tags=["Redemptions"],
    status_code=200,
    response_model=Redemption,
    response_description="The updated redemption",
)
def update_redemption(
    identity: Identity = Depends(identity_with_account),
    redemption_id: str = PathParams.CONTACT_ID,
    redemption_update: RedemptionUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption = versify.redemptions.get(redemption_id)
    if not redemption:
        raise NotFoundException()
    if redemption.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.redemptions.update(redemption_id, redemption_update.dict())
    return update_result


@router.delete(
    path="/{redemption_id}",
    summary="Delete redemption",
    description="Delete an redemption",
    tags=["Redemptions"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted redemption",
)
def delete_redemption(
    identity: Identity = Depends(identity_with_account),
    redemption_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    redemption = versify.redemptions.get(redemption_id)
    if not redemption:
        raise NotFoundException()
    if redemption.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.redemptions.delete(redemption_id)
    return delete_result
