from fastapi import APIRouter, Depends

from ....crud import versify
from ....models.enums import TeamMemberRole
from ....models.message import Message, MessageCreate, MessageUpdate
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

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get(
    path="",
    summary="List messages",
    description="List messages with optional filters and pagination parameters",
    tags=["Messages"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of messages",
)
def list_messages(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.messages.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    messages = versify.messages.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": messages, "has_more": count > len(messages)}


@router.post(
    path="/search",
    summary="Search messages",
    description="Search messages with query string",
    tags=["Messages"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of messages",
)
def search_messages(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    messages = versify.messages.search(account=identity.account.id, query=query)
    return {"count": len(messages), "data": messages}


@router.post(
    path="",
    summary="Create message",
    description="Create a message",
    tags=["Messages"],
    status_code=201,
    response_model=Message,
    response_description="The created message",
)
def create_message(
    identity: Identity = Depends(identity_with_account),
    message_create: MessageCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = message_create.dict()
    body["account"] = identity.account.id
    create_result = versify.messages.create(body)
    return create_result


@router.get(
    path="/{message_id}",
    summary="Get message",
    description="Get a message",
    tags=["Messages"],
    status_code=200,
    response_model=Message,
    response_description="The message",
)
def get_message(
    identity: Identity = Depends(identity_with_account),
    message_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    message = versify.messages.get(message_id)
    if not message:
        raise NotFoundException("Message not found")
    if message.account != identity.account.id:
        raise ForbiddenException()
    return message


@router.put(
    path="/{message_id}",
    summary="Update message",
    description="Update an message",
    tags=["Messages"],
    status_code=200,
    response_model=Message,
    response_description="The updated message",
)
def update_message(
    identity: Identity = Depends(identity_with_account),
    message_id: str = PathParams.CONTACT_ID,
    message_update: MessageUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    message = versify.messages.get(message_id)
    if not message:
        raise NotFoundException()
    if message.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.messages.update(message_id, message_update.dict())
    return update_result


@router.delete(
    path="/{message_id}",
    summary="Delete message",
    description="Delete an message",
    tags=["Messages"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted message",
)
def delete_message(
    identity: Identity = Depends(identity_with_account),
    message_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    message = versify.messages.get(message_id)
    if not message:
        raise NotFoundException()
    if message.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.messages.delete(message_id)
    return delete_result
