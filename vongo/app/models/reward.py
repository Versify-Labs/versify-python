from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.enums import RewardType
from app.models.factory import current_timestamp, reward_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Reward(Base):
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
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the reward was created",
        example=1601059200,
        title="Created Timestamp",
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
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata for the reward",
        title="Metadata",
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
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the reward was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )


class RewardCreateRequest(Base):
    """A reward create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the reward",
        example={"key": "value"},
        title="Metadata",
    )


class RewardCreateResponse(Reward):
    """A reward create response body."""

    pass


class RewardDeleteRequest:
    """A reward delete request body."""

    pass


class RewardDeleteResponse(Base):
    """A reward delete response body."""

    id: str = Field(
        description="Unique identifier for the reward",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Reward ID",
    )
    object: str = Field(
        default="reward",
        description="The object type",
        example="reward",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the reward has been deleted",
        example=True,
        title="Deleted",
    )


class RewardGetRequest:
    """A reward get request body."""

    pass


class RewardGetResponse(Reward):
    """A reward get response body."""

    pass


class RewardListRequest:
    """A reward list request body."""

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
            description="The number of rewards to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class RewardListResponse(Base):
    """A reward list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of rewards returned",
        example=1,
        title="Count",
    )
    data: List[Reward] = Field(
        default=[],
        description="The list of rewards that match the filters and pagination parameters.",
        title="Rewards",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more rewards to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/rewards",
        description="The URL of the list request",
        example="/v1/rewards",
        title="URL",
    )


class RewardSearchRequest(Base):
    """A reward search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class RewardSearchResponse(Base):
    """A reward search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of rewards returned",
        example=1,
        title="Count",
    )
    data: List[Reward] = Field(
        default=[],
        description="The list of rewards that match the filters and pagination parameters.",
        title="Rewards",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more rewards to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/rewards/search",
        description="The URL of the search request",
        example="/v1/rewards/search",
        title="URL",
    )


class RewardUpdateRequest(Base):
    """A reward update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the reward",
        example={"key": "value"},
        title="Metadata",
    )


class RewardUpdateResponse(Reward):
    """A reward update response body."""

    pass
