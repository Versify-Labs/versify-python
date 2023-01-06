from enum import Enum
from typing import Optional

from ._base import BaseAccountModel, BaseModel


class JourneyRunStatus(str, Enum):
    RUNNING = 'journey_running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class JourneyRunListItem(BaseModel):
    name: str
    result: dict = {}
    status: JourneyRunStatus
    time_started: int
    time_ended: Optional[int]


class JourneyRun(BaseAccountModel):
    object: str = 'journey_run'
    contact: str
    journey: str
    results: dict[str, JourneyRunListItem] = {}
    status: JourneyRunStatus = JourneyRunStatus.RUNNING
    time_started: int
    time_ended: Optional[int]
    trigger_event: dict
