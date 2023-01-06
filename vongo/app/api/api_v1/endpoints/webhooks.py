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
from app.models.webhook import Webhook, WebhookCreate, WebhookUpdate

from app.models.enums import TeamMemberRole
from ...exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.get(
    path="",
    summary="List webhooks",
    description="List webhooks with optional filters and pagination parameters",
    tags=["Webhooks"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of webhooks",
)
def list_webhooks(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.webhooks.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    webhooks = versify.webhooks.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": webhooks, "has_more": count > len(webhooks)}


@router.post(
    path="/search",
    summary="Search webhooks",
    description="Search webhooks with query string",
    tags=["Webhooks"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of webhooks",
)
def search_webhooks(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    webhooks = versify.webhooks.search(account=identity.account.id, query=query)
    return {"count": len(webhooks), "data": webhooks}


@router.post(
    path="",
    summary="Create webhook",
    description="Create a webhook",
    tags=["Webhooks"],
    status_code=201,
    response_model=Webhook,
    response_description="The created webhook",
)
def create_webhook(
    identity: Identity = Depends(identity_with_account),
    webhook_create: WebhookCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = webhook_create.dict()
    body["account"] = identity.account.id
    create_result = versify.webhooks.create(body)
    return create_result


@router.get(
    path="/{webhook_id}",
    summary="Get webhook",
    description="Get a webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=Webhook,
    response_description="The webhook",
)
def get_webhook(
    identity: Identity = Depends(identity_with_account),
    webhook_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook = versify.webhooks.get(webhook_id)
    if not webhook:
        raise NotFoundException("Webhook not found")
    if webhook.account != identity.account.id:
        raise ForbiddenException()
    return webhook


@router.put(
    path="/{webhook_id}",
    summary="Update webhook",
    description="Update an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=Webhook,
    response_description="The updated webhook",
)
def update_webhook(
    identity: Identity = Depends(identity_with_account),
    webhook_id: str = PathParams.CONTACT_ID,
    webhook_update: WebhookUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook = versify.webhooks.get(webhook_id)
    if not webhook:
        raise NotFoundException()
    if webhook.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.webhooks.update(webhook_id, webhook_update.dict())
    return update_result


@router.delete(
    path="/{webhook_id}",
    summary="Delete webhook",
    description="Delete an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted webhook",
)
def delete_webhook(
    identity: Identity = Depends(identity_with_account),
    webhook_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    webhook = versify.webhooks.get(webhook_id)
    if not webhook:
        raise NotFoundException()
    if webhook.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.webhooks.delete(webhook_id)
    return delete_result
