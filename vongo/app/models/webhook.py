from typing import Optional

from pydantic import Field

from .base import Base
from .factory import current_timestamp, webhook_event_id, webhook_id


class Webhook(Base):
    id: str = Field(
        alias="_id",
        default_factory=webhook_id,
        description='Unique identifier for the webhook',
        example='wh_1234567890',
        title='Webhook ID'
    )
    object: str = Field(
        default='webhook',
        description='The object type',
        example='webhook',
        title='Object Type'
    )
    active: bool = Field(
        default=True,
        description='Whether the webhook is active',
        example=True,
        title='Active'
    )
    description: Optional[str] = Field(
        description='A description of the webhook',
        example='My webhook',
        title='Description'
    )
    enabled_events: list = Field(
        default=[],
        description='The events that will trigger the webhook',
        example=['contact.created'],
        title='Enabled Events'
    )
    updated: Optional[int] = Field(
        description='The timestamp when the webhook was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )
    url: str = Field(
        description='The URL that will receive the webhook',
        example='https://mywebhook.com',
        title='Webhook URL'
    )


class WebhookEvent(Base):
    id: str = Field(
        alias="_id",
        default_factory=webhook_event_id,
        description='Unique identifier for the webhook event',
        example='wvt_1234567890',
        title='Webhook Event ID'
    )
    object: str = Field(
        default='webhook_event',
        description='The object type',
        example='webhook_event',
        title='Object Type'
    )
    created: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the webhook event was created',
        example=1601059200,
        title='Created Timestamp'
    )
    data: dict = Field(
        default={},
        description='The data associated with the webhook event',
        title='Data'
    )
    event: str = Field(
        description='The event type',
        example='contact.created',
        title='Event Type'
    )
    metadata: dict = Field(
        default={},
        description='Arbitrary metadata for the webhook event',
        title='Metadata'
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the webhook event was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )
    webhook: str = Field(
        description='The webhook ID',
        example='wh_1234567890',
        title='Webhook ID'
    )
