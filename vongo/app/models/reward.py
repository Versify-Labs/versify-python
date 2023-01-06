from typing import Union

from app.models.base import BaseDoc, BaseCreate, BaseUpdate
from app.models.enums import RewardType
from app.models.factory import reward_id
from pydantic import Field


class Reward(BaseDoc):
    """A reward document in the database."""

    __db__ = "Dev"
    __collection__ = "Rewards"

    id: str = Field(
        alias="_id",
        default_factory=reward_id,
        description="Unique identifier for the reward",
        example="rwd_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Reward ID",
    )
    object: str = Field(
        default="reward",
        description='The object type. Always "reward"',
        example="reward",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the reward belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    active: bool = Field(
        default=True,
        description="Whether the reward is active",
        example=True,
        title="Active",
    )
    description: str = Field(
        default="",
        description="The description of the reward",
        example="A reward for doing something",
        title="Description",
    )
    image: Union[str, None] = Field(
        default=None,
        description="The image of the reward",
        example="https://example.com/image.png",
        title="Image",
    )
    name: str = Field(
        default="", description="The name of the reward", example="Reward", title="Name"
    )
    reward_type: RewardType = Field(
        default=RewardType.COUPON,
        description="The type of the reward",
        example=RewardType.COUPON,
        title="Type",
    )


class RewardCreate(BaseCreate):
    """A reward create request body."""

    pass


class RewardUpdate(BaseUpdate):
    """A reward update request body."""

    pass
