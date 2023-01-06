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
from app.models.user import User
from app.models.webhook import (
    WebhookCreateRequest,
    WebhookCreateResponse,
    WebhookDeleteResponse,
    WebhookGetResponse,
    WebhookListRequest,
    WebhookListResponse,
    WebhookSearchRequest,
    WebhookSearchResponse,
    WebhookUpdateRequest,
    WebhookUpdateResponse,
)
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.get(
    path="",
    summary="List webhooks",
    description="List webhooks with optional filters and pagination parameters",
    tags=["Webhooks"],
    status_code=200,
    response_model=WebhookListResponse,
    response_description="The list of webhooks",
)
def list_webhooks(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    webhook_list_request: WebhookListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.webhooks.count(
        account=current_account.id,
    )
    webhooks = versify.webhooks.list(
        page_num=webhook_list_request.page_num,
        page_size=webhook_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": webhooks, "has_more": count > len(webhooks)}


@router.post(
    path="/search",
    summary="Search webhooks",
    description="Search webhooks with query string",
    tags=["Webhooks"],
    status_code=200,
    response_model=WebhookSearchResponse,
    response_description="The list of webhooks",
)
def search_webhooks(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    webhook_search_request: WebhookSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook_search_request_dict = webhook_search_request.dict()
    query = webhook_search_request_dict["query"]
    webhooks = versify.webhooks.search(account=current_account.id, query=query)
    return {"count": len(webhooks), "data": webhooks}


@router.post(
    path="",
    summary="Create webhook",
    description="Create a webhook",
    tags=["Webhooks"],
    status_code=201,
    response_model=WebhookCreateResponse,
    response_description="The created webhook",
)
def create_webhook(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    webhook_create: WebhookCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = webhook_create.dict()
    body["account"] = current_account.id
    create_result = versify.webhooks.create(body)
    return create_result


@router.get(
    path="/{webhook_id}",
    summary="Get webhook",
    description="Get a webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=WebhookGetResponse,
    response_description="The webhook",
)
def get_webhook(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    webhook_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook = versify.webhooks.get(webhook_id)
    if not webhook:
        raise NotFoundException()
    if webhook.account != current_account.id:
        raise ForbiddenException()
    return webhook


@router.put(
    path="/{webhook_id}",
    summary="Update webhook",
    description="Update an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=WebhookUpdateResponse,
    response_description="The updated webhook",
)
def update_webhook(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    webhook_id: str = PathParams.CONTACT_ID,
    webhook_update: WebhookUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook = versify.webhooks.get(webhook_id)
    if not webhook:
        raise NotFoundException()
    if webhook.account != current_account.id:
        raise ForbiddenException()
    body = webhook_update.dict()
    update_result = versify.webhooks.update(webhook_id, body)
    return update_result


@router.delete(
    path="/{webhook_id}",
    summary="Delete webhook",
    description="Delete an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=WebhookDeleteResponse,
    response_description="The deleted webhook",
)
def delete_webhook(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    webhook_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook = versify.webhooks.get(webhook_id)
    if not webhook:
        raise NotFoundException()
    if webhook.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.webhooks.delete(webhook_id)
    return delete_result
