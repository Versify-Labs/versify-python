from enum import Enum
from typing import Optional

from pydantic import EmailStr

from ._base import BaseAccountModel


class MintStatus(str, Enum):
    RESERVED = "reserved"
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class Mint(BaseAccountModel):
    object: str = 'mint'
    airdrop: Optional[str]
    contact: Optional[str]
    email: Optional[EmailStr]
    journey: Optional[str]
    journey_run: Optional[str]
    mint_link: Optional[str]
    product: str
    reference_id: Optional[str]
    signature: Optional[str]
    status: MintStatus = MintStatus.RESERVED
    transaction: Optional[str]
    wallet_address: Optional[str]
