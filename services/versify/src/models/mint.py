from typing import Optional

from pydantic import EmailStr, Field

from ..interfaces.versify_model import BaseVersifyModel


class Mint(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'mint'
    airdrop: Optional[str]
    contact: Optional[str]
    created: int
    email: Optional[EmailStr]
    metadata: Optional[dict] = {}
    mint_link: Optional[str]
    product: str
    reference_id: Optional[str]
    signature: Optional[str]
    # updates to pending, then failed or complete once we receive transaction result
    status: str = 'reserved'
    transaction: Optional[str]
    updated: Optional[int]
    wallet_address: Optional[str]
