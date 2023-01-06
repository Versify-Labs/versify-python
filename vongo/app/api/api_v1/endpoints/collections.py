from fastapi import APIRouter, Depends

from ....crud import versify
from ....models.collection import Collection, CollectionCreate, CollectionUpdate
from ....models.enums import TeamMemberRole
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

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get(
    path="",
    summary="List collections",
    description="List collections with optional filters and pagination parameters",
    tags=["Collections"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of collections",
)
def list_collections(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.collections.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    collections = versify.collections.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": collections, "has_more": count > len(collections)}


@router.post(
    path="/search",
    summary="Search collections",
    description="Search collections with query string",
    tags=["Collections"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of collections",
)
def search_collections(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    collections = versify.collections.search(account=identity.account.id, query=query)
    return {"count": len(collections), "data": collections}


@router.post(
    path="",
    summary="Create collection",
    description="Create a collection",
    tags=["Collections"],
    status_code=201,
    response_model=Collection,
    response_description="The created collection",
)
def create_collection(
    identity: Identity = Depends(identity_with_account),
    collection_create: CollectionCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = collection_create.dict()
    body["account"] = identity.account.id
    create_result = versify.collections.create(body)
    return create_result


@router.get(
    path="/{collection_id}",
    summary="Get collection",
    description="Get a collection",
    tags=["Collections"],
    status_code=200,
    response_model=Collection,
    response_description="The collection",
)
def get_collection(
    identity: Identity = Depends(identity_with_account),
    collection_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection = versify.collections.get(collection_id)
    if not collection:
        raise NotFoundException("Collection not found")
    if collection.account != identity.account.id:
        raise ForbiddenException()
    return collection


@router.put(
    path="/{collection_id}",
    summary="Update collection",
    description="Update an collection",
    tags=["Collections"],
    status_code=200,
    response_model=Collection,
    response_description="The updated collection",
)
def update_collection(
    identity: Identity = Depends(identity_with_account),
    collection_id: str = PathParams.CONTACT_ID,
    collection_update: CollectionUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection = versify.collections.get(collection_id)
    if not collection:
        raise NotFoundException()
    if collection.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.collections.update(collection_id, collection_update.dict())
    return update_result


@router.delete(
    path="/{collection_id}",
    summary="Delete collection",
    description="Delete an collection",
    tags=["Collections"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted collection",
)
def delete_collection(
    identity: Identity = Depends(identity_with_account),
    collection_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    collection = versify.collections.get(collection_id)
    if not collection:
        raise NotFoundException()
    if collection.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.collections.delete(collection_id)
    return delete_result
