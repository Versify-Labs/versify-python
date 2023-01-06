from typing import Union

from pydantic import Field

from .base import BaseCreate, BaseDoc, BaseUpdate
from .factory import redemption_id


class Redemption(BaseDoc):
    """A redemption document in the database."""

    __db__ = "Dev"
    __collection__ = "Redemptions"

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
    reward: str = Field(
        ...,
        description="The reward the redemption is for",
        example="rwd_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Reward ID",
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


class RedemptionCreate(BaseCreate):
    """A redemption create request body."""

    pass


class RedemptionUpdate(BaseUpdate):
    """A redemption update request body."""

    pass
