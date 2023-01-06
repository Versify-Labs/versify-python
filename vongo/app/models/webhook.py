from typing import Union

from app.models.base import BaseCreate, BaseDoc, BaseUpdate
from app.models.factory import webhook_id
from pydantic import Field


class Webhook(BaseDoc):
    """A webhook document in the database."""

    __db__ = "Dev"
    __collection__ = "Webhooks"

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
    url: str = Field(
        description="The URL that will receive the webhook",
        example="https://mywebhook.com",
        title="Webhook URL",
    )


class WebhookCreate(BaseCreate):
    """A webhook create request body."""

    pass


class WebhookUpdate(BaseUpdate):
    """A webhook update request body."""

    pass


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
