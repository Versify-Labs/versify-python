from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.tag import (
    TagCreateRequest,
    TagCreateResponse,
    TagDeleteResponse,
    TagGetResponse,
    TagListRequest,
    TagListResponse,
    TagSearchRequest,
    TagSearchResponse,
    TagUpdateRequest,
    TagUpdateResponse,
)
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get(
    path="",
    summary="List tags",
    description="List tags with optional filters and pagination parameters",
    tags=["Tags"],
    status_code=200,
    response_model=TagListResponse,
    response_description="The list of tags",
)
def list_tags(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    tag_list_request: TagListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.tags.count(
        account=current_account.id,
    )
    tags = versify.tags.list(
        page_num=tag_list_request.page_num,
        page_size=tag_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": tags, "has_more": count > len(tags)}


@router.post(
    path="/search",
    summary="Search tags",
    description="Search tags with query string",
    tags=["Tags"],
    status_code=200,
    response_model=TagSearchResponse,
    response_description="The list of tags",
)
def search_tags(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    tag_search_request: TagSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag_search_request_dict = tag_search_request.dict()
    query = tag_search_request_dict["query"]
    tags = versify.tags.search(account=current_account.id, query=query)
    return {"count": len(tags), "data": tags}


@router.post(
    path="",
    summary="Create tag",
    description="Create a tag",
    tags=["Tags"],
    status_code=201,
    response_model=TagCreateResponse,
    response_description="The created tag",
)
def create_tag(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    tag_create: TagCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = tag_create.dict()
    body["account"] = current_account.id
    create_result = versify.tags.create(body)
    return create_result


@router.get(
    path="/{tag_id}",
    summary="Get tag",
    description="Get a tag",
    tags=["Tags"],
    status_code=200,
    response_model=TagGetResponse,
    response_description="The tag",
)
def get_tag(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    tag_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag = versify.tags.get(tag_id)
    if not tag:
        raise NotFoundException()
    if tag.account != current_account.id:
        raise ForbiddenException()
    return tag


@router.put(
    path="/{tag_id}",
    summary="Update tag",
    description="Update an tag",
    tags=["Tags"],
    status_code=200,
    response_model=TagUpdateResponse,
    response_description="The updated tag",
)
def update_tag(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    tag_id: str = PathParams.CONTACT_ID,
    tag_update: TagUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag = versify.tags.get(tag_id)
    if not tag:
        raise NotFoundException()
    if tag.account != current_account.id:
        raise ForbiddenException()
    body = tag_update.dict()
    update_result = versify.tags.update(tag_id, body)
    return update_result


@router.delete(
    path="/{tag_id}",
    summary="Delete tag",
    description="Delete an tag",
    tags=["Tags"],
    status_code=200,
    response_model=TagDeleteResponse,
    response_description="The deleted tag",
)
def delete_tag(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    tag_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    tag = versify.tags.get(tag_id)
    if not tag:
        raise NotFoundException()
    if tag.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.tags.delete(tag_id)
    return delete_result
