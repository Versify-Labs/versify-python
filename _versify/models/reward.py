from enum import Enum
from typing import Optional

from ._base import BaseAccountModel


class RewardType(str, Enum):
    """Reward type enum."""
    COUPON = 'coupon'
    DISCOUNT = 'discount'
    GIFT = 'gift'


class Reward(BaseAccountModel):
    """Reward model."""
    object = 'reward'
    active: bool = True
    description: str = ''
    image: Optional[str]
    name: str = ''
    type: RewardType = RewardType.COUPON
