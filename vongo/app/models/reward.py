from typing import Any, Dict, Optional

from pydantic import Field

from .base import Base
from .enums import RewardType
from .factory import current_timestamp, reward_id


class Reward(Base):
    id: str = Field(
        alias="_id",
        default_factory=reward_id,
        description='Unique identifier for the reward',
        example='rwd_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Reward ID'
    )
    object: str = Field(
        default='reward',
        description='The object type. Always "reward"',
        example='reward',
        title='Object Type'
    )
    active: bool = Field(
        default=True,
        description='Whether the reward is active',
        example=True,
        title='Active'
    )
    description: str = Field(
        default='',
        description='The description of the reward',
        example='A reward for doing something',
        title='Description'
    )
    image: Optional[str] = Field(
        default=None,
        description='The image of the reward',
        example='https://example.com/image.png',
        title='Image'
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description='Arbitrary metadata associated with the reward',
        example={'key': 'value'},
        title='Metadata'
    )
    name: str = Field(
        default='',
        description='The name of the reward',
        example='Reward',
        title='Name'
    )
    type: RewardType = Field(
        default=RewardType.COUPON,
        description='The type of the reward',
        example=RewardType.COUPON,
        title='Type'
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the reward was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )
