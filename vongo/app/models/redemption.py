from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.factory import current_timestamp, redemption_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Redemption(Base):
    id: str = Field(
        alias="_id",
        default_factory=redemption_id,
        description="Unique identifier for the redemption",
        example="redemption_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Event ID",
    )
    object: str = Field(
        default="redemption",
        description='The object type. Always "redemption"',
        example="redemption",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the redemption belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    contact: str = Field(
        ...,
        description="The ID of the contact redeeming the reward.",
        title="Contact ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the redemption was created",
        example=1601059200,
        title="Created Timestamp",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the redemption",
        example={"key": "value"},
        title="Metadata",
    )
    reward: str = Field(
        ...,
        description="The reward the redemption is for",
        example="rwd_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Reward ID",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the redemption was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
    coupon_code: Union[str, None] = Field(
        default=None,
        description="The coupon code used to redeem the reward",
        example="ABC123",
        title="Coupon Code",
    )
    discount_code: Union[str, None] = Field(
        default=None,
        description="The discount code used to redeem the reward",
        example="ABC123",
        title="Discount Code",
    )
    discount_amount: Union[int, None] = Field(
        default=None,
        description="The amount of the discount used to redeem the reward",
        example=100,
        title="Discount Amount",
    )
    gift_code: Union[str, None] = Field(
        default=None,
        description="The gift code used to redeem the reward",
        example="ABC123",
        title="Gift Code",
    )
    gift_amount: Union[int, None] = Field(
        default=None,
        description="The amount of the gift used to redeem the reward",
        example=100,
        title="Gift Amount",
    )
    pass_platform: Union[str, None] = Field(
        default=None,
        description="The platform of the pass used to redeem the reward",
        example="apple",
        title="Pass Platform",
    )
    pass_barcode: Union[str, None] = Field(
        default=None,
        description="The barcode of the pass used to redeem the reward",
        example="ABC123",
        title="Pass Barcode",
    )
    pass_serial_number: Union[str, None] = Field(
        default=None,
        description="The serial number of the pass used to redeem the reward",
        example="ABC123",
        title="Pass Serial Number",
    )


class RedemptionCreateRequest(Base):
    """A redemption create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the redemption",
        example={"key": "value"},
        title="Metadata",
    )


class RedemptionCreateResponse(Redemption):
    """A redemption create response body."""

    pass


class RedemptionDeleteRequest:
    """A redemption delete request body."""

    pass


class RedemptionDeleteResponse(Base):
    """A redemption delete response body."""

    id: str = Field(
        description="Unique identifier for the redemption",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Redemption ID",
    )
    object: str = Field(
        default="redemption",
        description="The object type",
        example="redemption",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the redemption has been deleted",
        example=True,
        title="Deleted",
    )


class RedemptionGetRequest:
    """A redemption get request body."""

    pass


class RedemptionGetResponse(Redemption):
    """A redemption get response body."""

    pass


class RedemptionListRequest:
    """A redemption list request body."""

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
            description="The number of redemptions to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class RedemptionListResponse(Base):
    """A redemption list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of redemptions returned",
        example=1,
        title="Count",
    )
    data: List[Redemption] = Field(
        default=[],
        description="The list of redemptions that match the filters and pagination parameters.",
        title="Redemptions",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more redemptions to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/redemptions",
        description="The URL of the list request",
        example="/v1/redemptions",
        title="URL",
    )


class RedemptionSearchRequest(Base):
    """A redemption search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class RedemptionSearchResponse(Base):
    """A redemption search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of redemptions returned",
        example=1,
        title="Count",
    )
    data: List[Redemption] = Field(
        default=[],
        description="The list of redemptions that match the filters and pagination parameters.",
        title="Redemptions",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more redemptions to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/redemptions/search",
        description="The URL of the search request",
        example="/v1/redemptions/search",
        title="URL",
    )


class RedemptionUpdateRequest(Base):
    """A redemption update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the redemption",
        example={"key": "value"},
        title="Metadata",
    )


class RedemptionUpdateResponse(Redemption):
    """A redemption update response body."""

    pass
