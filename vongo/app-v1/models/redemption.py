from typing import Optional

from ._base import BaseAccountModel


class Redemption(BaseAccountModel):
    """Redemption model."""

    object = "redemption"
    contact: str
    coupon_code: Optional[str]
    discount_code: Optional[str]
    discount_amount: Optional[int]
    gift_code: Optional[str]
    gift_amount: Optional[int]
    pass_platform: Optional[str]
    pass_barcode: Optional[str]
    pass_serial_number: Optional[str]
    reward: str
