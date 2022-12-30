from typing import Any, Dict, Optional

from pydantic import Field

from .base import Base
from .factory import current_timestamp, redemption_id


class Redemption(Base):
    id: str = Field(
        alias="_id",
        default_factory=redemption_id,
        description='Unique identifier for the redemption',
        example='redemption_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Event ID'
    )
    object: str = Field(
        default='redemption',
        description='The object type. Always "redemption"',
        example='redemption',
        title='Object Type'
    )
    contact: str = Field(
        ...,
        description='The contact the redemption is for',
        title='Contact ID'
    )
    created: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the redemption was created',
        example=1601059200,
        title='Created Timestamp'
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description='Arbitrary metadata associated with the redemption',
        example={'key': 'value'},
        title='Metadata'
    )
    reward: str = Field(
        ...,
        description='The reward the redemption is for',
        example='rwd_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Reward ID'
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the redemption was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )
    # TODO: Imeplement redemption fields
    coupon_code: Optional[str]
    discount_code: Optional[str]
    discount_amount: Optional[int]
    gift_code: Optional[str]
    gift_amount: Optional[int]
    pass_platform: Optional[str]
    pass_barcode: Optional[str]
    pass_serial_number: Optional[str]
