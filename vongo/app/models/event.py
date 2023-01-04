from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.factory import current_timestamp, event_id
from app.models.globals import Query
from fastapi import Query as QueryParam
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
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the event was created",
        example=1601059200,
        title="Created Timestamp",
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


class EventCreateRequest(Base):
    """A event create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the event",
        example={"key": "value"},
        title="Metadata",
    )


class EventCreateResponse(Event):
    """A event create response body."""

    pass


class EventDeleteRequest:
    """A event delete request body."""

    pass


class EventDeleteResponse(Base):
    """A event delete response body."""

    id: str = Field(
        description="Unique identifier for the event",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Event ID",
    )
    object: str = Field(
        default="event",
        description="The object type",
        example="event",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the event has been deleted",
        example=True,
        title="Deleted",
    )


class EventGetRequest:
    """A event get request body."""

    pass


class EventGetResponse(Event):
    """A event get response body."""

    pass


class EventListRequest:
    """A event list request body."""

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
            description="The number of events to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class EventListResponse(Base):
    """A event list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of events returned",
        example=1,
        title="Count",
    )
    data: List[Event] = Field(
        default=[],
        description="The list of events that match the filters and pagination parameters.",
        title="Events",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more events to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/events",
        description="The URL of the list request",
        example="/v1/events",
        title="URL",
    )


class EventSearchRequest(Base):
    """A event search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class EventSearchResponse(Base):
    """A event search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of events returned",
        example=1,
        title="Count",
    )
    data: List[Event] = Field(
        default=[],
        description="The list of events that match the filters and pagination parameters.",
        title="Events",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more events to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/events/search",
        description="The URL of the search request",
        example="/v1/events/search",
        title="URL",
    )


class EventUpdateRequest(Base):
    """A event update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the event",
        example={"key": "value"},
        title="Metadata",
    )


class EventUpdateResponse(Event):
    """A event update response body."""

    pass
