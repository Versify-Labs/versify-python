from ...deps import identity_with_account
from app.crud import versify
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
from app.models.tag import Tag, TagCreate, TagUpdate

from app.models.enums import TeamMemberRole
from ...exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get(
    path="",
    summary="List tags",
    description="List tags with optional filters and pagination parameters",
    tags=["Tags"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of tags",
)
def list_tags(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.tags.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    tags = versify.tags.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": tags, "has_more": count > len(tags)}


@router.post(
    path="/search",
    summary="Search tags",
    description="Search tags with query string",
    tags=["Tags"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of tags",
)
def search_tags(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    tags = versify.tags.search(account=identity.account.id, query=query)
    return {"count": len(tags), "data": tags}


@router.post(
    path="",
    summary="Create tag",
    description="Create a tag",
    tags=["Tags"],
    status_code=201,
    response_model=Tag,
    response_description="The created tag",
)
def create_tag(
    identity: Identity = Depends(identity_with_account),
    tag_create: TagCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = tag_create.dict()
    body["account"] = identity.account.id
    create_result = versify.tags.create(body)
    return create_result


@router.get(
    path="/{tag_id}",
    summary="Get tag",
    description="Get a tag",
    tags=["Tags"],
    status_code=200,
    response_model=Tag,
    response_description="The tag",
)
def get_tag(
    identity: Identity = Depends(identity_with_account),
    tag_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag = versify.tags.get(tag_id)
    if not tag:
        raise NotFoundException("Tag not found")
    if tag.account != identity.account.id:
        raise ForbiddenException()
    return tag


@router.put(
    path="/{tag_id}",
    summary="Update tag",
    description="Update an tag",
    tags=["Tags"],
    status_code=200,
    response_model=Tag,
    response_description="The updated tag",
)
def update_tag(
    identity: Identity = Depends(identity_with_account),
    tag_id: str = PathParams.CONTACT_ID,
    tag_update: TagUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag = versify.tags.get(tag_id)
    if not tag:
        raise NotFoundException()
    if tag.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.tags.update(tag_id, tag_update.dict())
    return update_result


@router.delete(
    path="/{tag_id}",
    summary="Delete tag",
    description="Delete an tag",
    tags=["Tags"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted tag",
)
def delete_tag(
    identity: Identity = Depends(identity_with_account),
    tag_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag = versify.tags.get(tag_id)
    if not tag:
        raise NotFoundException()
    if tag.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.tags.delete(tag_id)
    return delete_result
