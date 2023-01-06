from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.collection import (
    CollectionCreateRequest,
    CollectionCreateResponse,
    CollectionDeleteResponse,
    CollectionGetResponse,
    CollectionListRequest,
    CollectionListResponse,
    CollectionSearchRequest,
    CollectionSearchResponse,
    CollectionUpdateRequest,
    CollectionUpdateResponse,
)
from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get(
    path="",
    summary="List collections",
    description="List collections with optional filters and pagination parameters",
    tags=["Collections"],
    status_code=200,
    response_model=CollectionListResponse,
    response_description="The list of collections",
)
def list_collections(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    collection_list_request: CollectionListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.collections.count(
        account=current_account.id,
    )
    collections = versify.collections.list(
        page_num=collection_list_request.page_num,
        page_size=collection_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": collections, "has_more": count > len(collections)}


@router.post(
    path="/search",
    summary="Search collections",
    description="Search collections with query string",
    tags=["Collections"],
    status_code=200,
    response_model=CollectionSearchResponse,
    response_description="The list of collections",
)
def search_collections(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    collection_search_request: CollectionSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection_search_request_dict = collection_search_request.dict()
    query = collection_search_request_dict["query"]
    collections = versify.collections.search(account=current_account.id, query=query)
    return {"count": len(collections), "data": collections}


@router.post(
    path="",
    summary="Create collection",
    description="Create a collection",
    tags=["Collections"],
    status_code=201,
    response_model=CollectionCreateResponse,
    response_description="The created collection",
)
def create_collection(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    collection_create: CollectionCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = collection_create.dict()
    body["account"] = current_account.id
    create_result = versify.collections.create(body)
    return create_result


@router.get(
    path="/{collection_id}",
    summary="Get collection",
    description="Get a collection",
    tags=["Collections"],
    status_code=200,
    response_model=CollectionGetResponse,
    response_description="The collection",
)
def get_collection(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    collection_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection = versify.collections.get(collection_id)
    if not collection:
        raise NotFoundException()
    if collection.account != current_account.id:
        raise ForbiddenException()
    return collection


@router.put(
    path="/{collection_id}",
    summary="Update collection",
    description="Update an collection",
    tags=["Collections"],
    status_code=200,
    response_model=CollectionUpdateResponse,
    response_description="The updated collection",
)
def update_collection(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    collection_id: str = PathParams.CONTACT_ID,
    collection_update: CollectionUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection = versify.collections.get(collection_id)
    if not collection:
        raise NotFoundException()
    if collection.account != current_account.id:
        raise ForbiddenException()
    body = collection_update.dict()
    update_result = versify.collections.update(collection_id, body)
    return update_result


@router.delete(
    path="/{collection_id}",
    summary="Delete collection",
    description="Delete an collection",
    tags=["Collections"],
    status_code=200,
    response_model=CollectionDeleteResponse,
    response_description="The deleted collection",
)
def delete_collection(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    collection_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection = versify.collections.get(collection_id)
    if not collection:
        raise NotFoundException()
    if collection.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.collections.delete(collection_id)
    return delete_result
