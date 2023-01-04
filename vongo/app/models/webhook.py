from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.factory import current_timestamp, webhook_event_id, webhook_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Webhook(Base):
    id: str = Field(
        alias="_id",
        default_factory=webhook_id,
        description="Unique identifier for the webhook",
        example="wh_1234567890",
        title="Webhook ID",
    )
    object: str = Field(
        default="webhook",
        description="The object type",
        example="webhook",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the webhook belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    active: bool = Field(
        default=True,
        description="Whether the webhook is active",
        example=True,
        title="Active",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the webhook was created",
        example=1601059200,
        title="Created Timestamp",
    )
    description: Union[str, None] = Field(
        description="A description of the webhook",
        example="My webhook",
        title="Description",
    )
    enabled_events: list = Field(
        default=[],
        description="The events that will trigger the webhook",
        example=["contact.created"],
        title="Enabled Events",
    )
    metadata: dict = Field(
        default={},
        description="Arbitrary metadata for the webhook",
        title="Metadata",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the webhook was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
    url: str = Field(
        description="The URL that will receive the webhook",
        example="https://mywebhook.com",
        title="Webhook URL",
    )


# class WebhookEvent(Base):
#     id: str = Field(
#         alias="_id",
#         default_factory=webhook_event_id,
#         description="Unique identifier for the webhook event",
#         example="wvt_1234567890",
#         title="Webhook Event ID",
#     )
#     object: str = Field(
#         default="webhook_event",
#         description="The object type",
#         example="webhook_event",
#         title="Object Type",
#     )
#     created: int = Field(
#         default_factory=current_timestamp,
#         description="The timestamp when the webhook event was created",
#         example=1601059200,
#         title="Created Timestamp",
#     )
#     data: dict = Field(
#         default={},
#         description="The data associated with the webhook event",
#         title="Data",
#     )
#     event: str = Field(
#         description="The type of event that triggered the webhook",
#         example="contact.created",
#         title="Event Type",
#     )
#     metadata: dict = Field(
#         default={},
#         description="Arbitrary metadata for the webhook event",
#         title="Metadata",
#     )
#     updated: int = Field(
#         default_factory=current_timestamp,
#         description="The timestamp when the webhook event was last updated",
#         example=1601059200,
#         title="Updated Timestamp",
#     )
#     webhook: str = Field(
#         description="The ID of the webhook that the event was sent to",
#         example="web_1234567890",
#         title="Webhook ID",
#     )


class WebhookCreateRequest(Base):
    """A webhook create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the web",
        example={"key": "value"},
        title="Metadata",
    )


class WebhookCreateResponse(Webhook):
    """A webhook create response body."""

    pass


class WebhookDeleteRequest:
    """A webhook delete request body."""

    pass


class WebhookDeleteResponse(Base):
    """A webhook delete response body."""

    id: str = Field(
        description="Unique identifier for the webhook",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Webhook ID",
    )
    object: str = Field(
        default="webhook",
        description="The object type",
        example="webhook",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the webhook has been deleted",
        example=True,
        title="Deleted",
    )


class WebhookGetRequest:
    """A webhook get request body."""

    pass


class WebhookGetResponse(Webhook):
    """A webhook get response body."""

    pass


class WebhookListRequest:
    """A webhook list request body."""

    def __init__(
        self,
        page_num: int = QueryParam(
            default=1,
            description="The page number to return",
            example=1,
            title="Page Number",
        ),
        page_size: int = QueryParam(
            default=20,
            description="The number of webhooks to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class WebhookListResponse(Base):
    """A webhook list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of webhooks returned",
        example=1,
        title="Count",
    )
    data: List[Webhook] = Field(
        default=[],
        description="The list of webhooks that match the filters and pagination parameters.",
        title="Webhooks",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more webhooks to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/webhooks",
        description="The URL of the list request",
        example="/v1/webhooks",
        title="URL",
    )


class WebhookSearchRequest(Base):
    """A webhook search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class WebhookSearchResponse(Base):
    """A webhook search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of webhooks returned",
        example=1,
        title="Count",
    )
    data: List[Webhook] = Field(
        default=[],
        description="The list of webhooks that match the filters and pagination parameters.",
        title="Webhooks",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more webhooks to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/webhooks/search",
        description="The URL of the search request",
        example="/v1/webhooks/search",
        title="URL",
    )


class WebhookUpdateRequest(Base):
    """A webhook update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the webhook",
        example={"key": "value"},
        title="Metadata",
    )


class WebhookUpdateResponse(Webhook):
    """A webhook update response body."""

    pass
