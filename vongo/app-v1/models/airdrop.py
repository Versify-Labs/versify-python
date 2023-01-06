from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ._base import BaseAccountModel


class EmailSettings(BaseModel):
    """Settings used to configure the airdrop's email notifications"""

    content: Optional[str] = "Claim your free NFT."
    from_email: Optional[str] = "airdrops@versifylabs.com"
    from_image: Optional[str]
    from_name: Optional[str] = "Versify Labs"
    preview_text: Optional[str] = "Claim your free NFT"
    subject_line: Optional[str] = "Claim your free NFT"


class Recipients(BaseModel):
    count: int = 0
    segment_options: dict = {"conditions": "", "match": "all"}
    emails_included: Optional[list] = []
    emails_excluded: Optional[list] = []
    tags_included: Optional[list] = []
    tags_excluded: Optional[list] = []


class AirdropStatus(str, Enum):
    DRAFT = "draft"
    SENDING = "sending"
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    CANCELLED = "cancelled"


class Airdrop(BaseAccountModel):
    """Airdrop model."""

    object: str = "airdrop"
    archived: Optional[bool] = False
    email_settings: Optional[EmailSettings]
    mint_link: Optional[str]
    name: str = "Untitled Airdrop"
    product: str
    recipients: Optional[Recipients]
    status: AirdropStatus = AirdropStatus.DRAFT
