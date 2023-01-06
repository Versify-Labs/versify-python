from typing import Any, Dict, Union

from app.models.base import BaseCreate, BaseDoc, BaseUpdate
from app.models.factory import event_id
from pydantic import Field


class Event(BaseDoc):
    """An event document in the database."""

    __db__ = "Dev"
    __collection__ = "Events"

    id: str = Field(
        alias="_id",
        default_factory=event_id,
        description="Unique identifier for the event",
        example="event_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Event ID",
    )
    object: str = Field(
        default="event",
        description='The object type. Always "event"',
        example="event",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the event belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    contact: Union[str, None] = Field(
        default=None,
        description="The contact the event is for",
        example="contact_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    detail_type: str = Field(
        ...,
        description="The type of event. For example, order.placed.",
        example="event_type",
        title="Event Type",
    )
    detail: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the event",
        example={"key": "value"},
        title="Metadata",
    )
    source: str = Field(
        default="versify",
        description="The source of the event",
        example="versify",
        title="Source",
    )


class EventCreate(BaseCreate):
    """A event create request body."""

    pass


class EventUpdate(BaseUpdate):
    """A event update request body."""

    pass
