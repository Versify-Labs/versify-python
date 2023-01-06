from typing import Union

from app.models.base import BaseCreate, BaseDoc, BaseUpdate
from app.models.enums import RunStatus
from app.models.factory import current_timestamp, journey_id, run_id
from app.models.globals import Action, RunStateResult, Trigger
from pydantic import Field


class Journey(BaseDoc):
    """A journey document in the database."""

    __db__ = "Dev"
    __collection__ = "Journeys"

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
    description: str = Field(
        default="",
        description="A description of the journey",
        example="My journey",
        title="Description",
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


class JourneyCreate(BaseCreate):
    """A journey create request body."""

    pass


class JourneyUpdate(BaseUpdate):
    """A journey update request body."""

    pass


class Run(BaseDoc):
    """A run of a journey."""

    __db__ = "Dev"
    __collection__ = "Runs"

    id: str = Field(
        alias="_id",
        default_factory=run_id,
        description="Unique identifier for the run",
        example="run_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Journey Run ID",
    )
    object: str = Field(
        default="run",
        description='The object type. Always "run"',
        example="run",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the journey belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    results: dict[str, RunStateResult] = Field(
        default={},
        description="The results of the run",
        example={"key": "value"},
        title="Results",
    )
    status: RunStatus = Field(
        default=RunStatus.RUNNING,
        description="The status of the run",
        example=RunStatus.RUNNING,
        title="Status",
    )
    time_started: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the run was started",
        example=1601059200,
        title="Started Timestamp",
    )
    time_ended: Union[int, None] = Field(
        default=None,
        description="The timestamp when the run was ended",
        example=1601059200,
        title="Ended Timestamp",
    )
    trigger_event: dict = Field(
        default={},
        description="The event that triggered the run",
        example={"key": "value"},
        title="Trigger Event",
    )
