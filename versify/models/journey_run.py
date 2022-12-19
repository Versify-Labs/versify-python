from enum import Enum
from typing import Optional

from ._base import BaseAccountModel, BaseModel


class RunStatus(str, Enum):
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class RunListItem(BaseModel):
    name: str
    result: dict = {}
    status: RunStatus
    time_started: int
    time_ended: Optional[int]


class JourneyRun(BaseAccountModel):
    object: str = 'journey_run'
    contact: str
    journey: str
    results: dict[str, RunListItem] = {}
    status: RunStatus = RunStatus.RUNNING
    time_started: int
    time_ended: Optional[int]
    trigger_event: dict
