from enum import Enum
from typing import Optional

from ._base import BaseAccountModel


class ClaimStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class Claim(BaseAccountModel):
    object: str = 'claim'
    code: str
    contact: Optional[str]
    product: str
    quantity: int = 1
    status: str = ClaimStatus.REQUESTED
