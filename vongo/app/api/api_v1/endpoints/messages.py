from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.message import (
    MessageCreateRequest,
    MessageCreateResponse,
    MessageDeleteRequest,
    MessageDeleteResponse,
    MessageGetRequest,
    MessageGetResponse,
    MessageListRequest,
    MessageListResponse,
    MessageSearchRequest,
    MessageSearchResponse,
    MessageUpdateRequest,
    MessageUpdateResponse,
)
from app.models.enums import TeamMemberRole
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get(
    path="",
    summary="List messages",
    description="List messages with optional filters and pagination parameters",
    tags=["Messages"],
    status_code=200,
    response_model=MessageListResponse,
    response_description="The list of messages",
)
def list_messages(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    message_list_request: MessageListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to list messages.",
        )
    count = versify.messages.count(
        account=current_account.id,
    )
    messages = versify.messages.list(
        page_num=message_list_request.page_num,
        page_size=message_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": messages, "has_more": count > len(messages)}


@router.post(
    path="/search",
    summary="Search messages",
    description="Search messages with query string",
    tags=["Messages"],
    status_code=200,
    response_model=MessageSearchResponse,
    response_description="The list of messages",
)
def search_messages(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    message_search_request: MessageSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to search messages.",
        )
    message_search_request_dict = message_search_request.dict()
    query = message_search_request_dict["query"]
    messages = versify.messages.search(account=current_account.id, query=query)
    return {"count": len(messages), "data": messages}


@router.post(
    path="",
    summary="Create message",
    description="Create a message",
    tags=["Messages"],
    status_code=201,
    response_model=MessageCreateResponse,
    response_description="The created message",
)
def create_message(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    message_create: MessageCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create messages.",
        )
    body = message_create.dict()
    body["account"] = current_account.id
    create_result = versify.messages.create(body)
    return create_result


@router.get(
    path="/{message_id}",
    summary="Get message",
    description="Get a message",
    tags=["Messages"],
    status_code=200,
    response_model=MessageGetResponse,
    response_description="The message",
)
def get_message(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    message_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view messages.",
        )
    message = versify.messages.get(message_id)
    if not message:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    if message.account != current_account.id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view messages for this account.",
        )
    return message


@router.put(
    path="/{message_id}",
    summary="Update message",
    description="Update an message",
    tags=["Messages"],
    status_code=200,
    response_model=MessageUpdateResponse,
    response_description="The updated message",
)
def update_message(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    message_id: str = PathParams.CONTACT_ID,
    message_update: MessageUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update messages.",
        )
    message = versify.messages.get(message_id)
    if not message:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    if message.account != current_account.id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update messages for this account.",
        )
    body = message_update.dict()
    update_result = versify.messages.update(message_id, body)
    return update_result


@router.delete(
    path="/{message_id}",
    summary="Delete message",
    description="Delete an message",
    tags=["Messages"],
    status_code=200,
    response_model=MessageDeleteResponse,
    response_description="The deleted message",
)
def delete_message(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    message_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete messages.",
        )
    message = versify.messages.get(message_id)
    if not message:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    if message.account != current_account.id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete messages for this account.",
        )
    delete_result = versify.messages.delete(message_id)
    return delete_result
