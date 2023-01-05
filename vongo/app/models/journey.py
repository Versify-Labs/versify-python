from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.factory import current_timestamp, journey_id
from app.models.globals import Action, Query, Trigger
from fastapi import Query as QueryParam
from pydantic import Field


class Journey(Base):
    id: str = Field(
        alias="_id",
        default_factory=journey_id,
        description="Unique identifier for the journey",
        example="j_1234567890",
        title="Journey ID",
    )
    object: str = Field(
        default="journey",
        description='The object type. Always "journey"',
        example="journey",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the journey belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    active: bool = Field(
        default=True,
        description="Whether the journey is active",
        example=True,
        title="Active",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the journey was created",
        example=1600000000,
        title="Created",
    )
    description: str = Field(
        default="",
        description="A description of the journey",
        example="My journey",
        title="Description",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the journey",
        example={"key": "value"},
        title="Metadata",
    )
    name: str = Field(
        description="The name of the journey. Internal facing.",
        example="My Journey",
        title="Name",
    )
    start: str = Field(
        default="start",
        description="The starting state of the journey",
        example="start",
        title="Start",
    )
    states: dict[str, Action] = Field(
        default_factory=dict,
        description="The states of the journey",
        example={
            "state_1": {
                "action_type": "create_note",
                "config": {"note": "This is a note"},
            },
            "state_2": {
                "action_type": "send_email_message",
                "config": {
                    "body": "This is an email",
                    "subject": "This is an email subject",
                },
            },
        },
        title="States",
    )
    trigger: Trigger = Field(
        ...,
        description="The trigger for the journey",
        example={
            "trigger_type": "event",
            "config": {
                "source": "contact",
                "detail_type": "contact.created",
                "detail_filters": [],
            },
        },
        title="Trigger",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the journey was last updated",
        example=1600000000,
        title="Updated",
    )


# class JourneyRun(Base):
#     id: str = Field(
#         alias="_id",
#         default_factory=journey_run_id,
#         description="Unique identifier for the journey_run",
#         example="journey_run_5f9f1c5b0b9b4b0b9c1c5b0b",
#         title="Event ID",
#     )
#     object: str = Field(
#         default="journey_run",
#         description='The object type. Always "journey_run"',
#         example="journey_run",
#         title="Object Type",
#     )
#     account: str = Field(
#         ...,
#         description="The account the journey belongs to",
#         example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
#         title="Account ID",
#     )
#     created: int = Field(
#         default_factory=current_timestamp,
#         description="The timestamp when the journey_run was created",
#         example=1601059200,
#         title="Created Timestamp",
#     )
#     metadata: Dict[str, Any] = Field(
#         default={},
#         description="Arbitrary metadata associated with the journey_run",
#         example={"key": "value"},
#         title="Metadata",
#     )
#     updated: int = Field(
#         default_factory=current_timestamp,
#         description="The timestamp when the journey_run was last updated",
#         example=1601059200,
#         title="Updated Timestamp",
#     )
#     results: dict[str, RunStateResult] = Field(
#         default={},
#         description="The results of the journey_run",
#         example={"key": "value"},
#         title="Results",
#     )
#     status: RunStatus = Field(
#         default=RunStatus.RUNNING,
#         description="The status of the journey_run",
#         example=RunStatus.RUNNING,
#         title="Status",
#     )
#     time_started: int = Field(
#         default_factory=current_timestamp,
#         description="The timestamp when the journey_run was started",
#         example=1601059200,
#         title="Started Timestamp",
#     )
#     time_ended: Union[int, None] = Field(
#         default=None,
#         description="The timestamp when the journey_run was ended",
#         example=1601059200,
#         title="Ended Timestamp",
#     )
#     trigger_event: dict = Field(
#         default={},
#         description="The event that triggered the journey_run",
#         example={"key": "value"},
#         title="Trigger Event",
#     )


class JourneyCreateRequest(Base):
    """A journey create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the journey",
        example={"key": "value"},
        title="Metadata",
    )


class JourneyCreateResponse(Journey):
    """A journey create response body."""

    pass


class JourneyDeleteRequest:
    """A journey delete request body."""

    pass


class JourneyDeleteResponse(Base):
    """A journey delete response body."""

    id: str = Field(
        description="Unique identifier for the journey",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Journey ID",
    )
    object: str = Field(
        default="journey",
        description="The object type",
        example="journey",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the journey has been deleted",
        example=True,
        title="Deleted",
    )


class JourneyGetRequest:
    """A journey get request body."""

    pass


class JourneyGetResponse(Journey):
    """A journey get response body."""

    pass


class JourneyListRequest:
    """A journey list request body."""

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
            description="The number of journeys to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class JourneyListResponse(Base):
    """A journey list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of journeys returned",
        example=1,
        title="Count",
    )
    data: List[Journey] = Field(
        default=[],
        description="The list of journeys that match the filters and pagination parameters.",
        title="Journeys",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more journeys to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/journeys",
        description="The URL of the list request",
        example="/v1/journeys",
        title="URL",
    )


class JourneySearchRequest(Base):
    """A journey search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class JourneySearchResponse(Base):
    """A journey search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of journeys returned",
        example=1,
        title="Count",
    )
    data: List[Journey] = Field(
        default=[],
        description="The list of journeys that match the filters and pagination parameters.",
        title="Journeys",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more journeys to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/journeys/search",
        description="The URL of the search request",
        example="/v1/journeys/search",
        title="URL",
    )


class JourneyUpdateRequest(Base):
    """A journey update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the journey",
        example={"key": "value"},
        title="Metadata",
    )


class JourneyUpdateResponse(Journey):
    """A journey update response body."""

    pass
