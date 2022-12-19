from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from ._base import BaseAccountModel


class Operator(str, Enum):

    # General
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'
    EXISTS = 'exists'
    NOT_EXISTS = 'not_exists'

    # String
    STARTS_WITH = 'starts_with'
    NOT_STARTS_WITH = 'not_starts_with'
    ENDS_WITH = 'ends_with'
    NOT_ENDS_WITH = 'not_ends_with'

    # Number
    GREATER_THAN = 'greater_than'
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal'
    LESS_THAN = 'less_than'
    LESS_THAN_OR_EQUAL = 'less_than_or_equal'


class Filter(BaseModel):
    """Filter model."""
    field: str
    operator: Operator = Operator.EQUAL
    value: Optional[Union[str, int, float, bool]]


"""
Offer
"""


class Offer(BaseModel):
    """Offer model."""
    name: Optional[str] = ''
    description: Optional[str] = ''
    image: Optional[str] = ''
    cta_text: Optional[str] = ''
    cta_url: Optional[str] = ''


"""
Triggers
"""


class TriggerType(str, Enum):
    EVENT = 'event'
    SCHEDULE = 'schedule'


class TriggerScheduleConfig(BaseModel):
    at: Optional[int]  # Ex: '1601514370'
    cron: Optional[str]  # Ex: '0 20 * * ? *'
    rate: Optional[str]  # Ex: '5 minutes'
    start: Optional[int]  # Ex: 1601514370
    end: Optional[int]  # Ex: 1601514370


class TriggerConfig(BaseModel):
    schedule: Optional[TriggerScheduleConfig]
    source: str
    detail_type: str
    detail_filters: list[Filter] = []


class Trigger(BaseModel):
    type: TriggerType
    config: TriggerConfig


"""
Actions
"""


class ActionType(str, Enum):
    """The status of a message."""

    # actions
    CREATE_NOTE = 'create_note'
    SEND_APP_MESSAGE = 'send_app_message'
    SEND_EMAIL_MESSAGE = 'send_email_message'
    SEND_REWARD = 'send_reward'
    TAG_CONTACT = 'tag_contact'

    # conditions
    MATCH_ALL = 'match_all'
    MATCH_ANY = 'match_any'
    WAIT = 'wait'


class ActionConfig(BaseModel):

    # CREATE_NOTE
    note: Optional[str]

    # SEND_APP_MESSAGE / SEND_EMAIL_MESSAGE
    body: Optional[str]
    member: Optional[str]
    subject: Optional[str]
    type: Optional[str]

    # SEND_REWARD
    product: Optional[str]
    quantity: Optional[int]

    # TAG_CONTACT
    tags: Optional[list[str]]

    # MATCH_ALL/MATCH_ANY
    filters: list[Filter] = []

    # WAIT
    seconds: Optional[int]


class Action(BaseModel):
    type: ActionType
    comment: Optional[str]
    config: ActionConfig
    end: Optional[bool]
    next: Optional[str]


"""
Journey
"""


class Journey(BaseAccountModel):
    object: str = 'journey'
    active: bool = False
    name: str
    offer: Optional[Offer]
    trigger: Trigger
    start: str
    states: dict[str, Action]
