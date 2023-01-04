from typing import Any, Dict, Optional

from app.models.base import Base
from app.models.factory import current_timestamp, event_id
from pydantic import Field


class Event(Base):
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
    contact: Optional[str] = Field(
        default=None,
        description="The contact the event is for",
        example="contact_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the event was created",
        example=1601059200,
        title="Created Timestamp",
    )
    detail_type: str = Field(
        ..., description="The type of event", example="event_type", title="Event Type"
    )
    detail: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the event",
        example={"key": "value"},
        title="Metadata",
    )
    metadata: Dict[str, Any] = Field(
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
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the event was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
