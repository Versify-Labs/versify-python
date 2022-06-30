from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Mint(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'mint'
    airdrop: Optional[str]
    contact: str
    created: int
    failure_code: Optional[int]
    failure_message: Optional[str]
    metadata: Optional[dict] = {}
    mint_link: Optional[str]
    organization: str
    product: str
    signature: Optional[str]
    status: str = 'reserved'  # reserved -> fulfilled -> complete / failed
    transaction: Optional[str]
    url: str  # example: "https://mint.versifylabs.com/{id}"
    wallet_address: Optional[str]
