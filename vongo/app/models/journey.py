from typing import Any, Dict, Optional

from pydantic import Field

from .base import Base
from .enums import RunStatus
from .factory import current_timestamp, journey_id, journey_run_id
from .globals import Action, RunStateResult, Trigger


class JourneyRun(Base):
    id: str = Field(
        alias="_id",
        default_factory=journey_run_id,
        description="Unique identifier for the journey_run",
        example="journey_run_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Event ID",
    )
    object: str = Field(
        default="journey_run",
        description='The object type. Always "journey_run"',
        example="journey_run",
        title="Object Type",
    )
    contact: str = Field(
        ..., description="The contact the journey_run is for", title="Contact ID"
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the journey_run was created",
        example=1601059200,
        title="Created Timestamp",
    )
    journey: str = Field(
        ..., description="The journey the journey_run is for", title="Journey ID"
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the journey_run",
        example={"key": "value"},
        title="Metadata",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the journey_run was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
    results: dict[str, RunStateResult] = Field(
        default={},
        description="The results of the journey_run",
        example={"key": "value"},
        title="Results",
    )
    status: RunStatus = Field(
        default=RunStatus.RUNNING,
        description="The status of the journey_run",
        example=RunStatus.RUNNING,
        title="Status",
    )
    time_started: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the journey_run was started",
        example=1601059200,
        title="Started Timestamp",
    )
    time_ended: Optional[int] = Field(
        default=None,
        description="The timestamp when the journey_run was ended",
        example=1601059200,
        title="Ended Timestamp",
    )
    trigger_event: dict = Field(
        default={},
        description="The event that triggered the journey_run",
        example={"key": "value"},
        title="Trigger Event",
    )


class Journey(Base):
    id: str = Field(
        alias="_id",
        default_factory=journey_id,
        description="Unique identifier for the journey",
        example="j_1234567890",
        title="Journey ID",
    )
    active: bool = Field(
        default=True,
        description="Whether the journey is active",
        example=True,
        title="Active",
    )
    description: Optional[str] = Field(
        default="",
        description="A description of the journey",
        example="My journey",
        title="Description",
    )
    name: str = Field(
        description="The name of the journey", example="My Journey", title="Name"
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
            "state_1": {"type": "create_note", "config": {"note": "This is a note"}},
            "state_2": {
                "type": "send_email_message",
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
            "type": "event",
            "config": {
                "source": "contact",
                "detail_type": "contact.created",
                "detail_filters": [],
            },
        },
        title="Trigger",
    )
