from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseVersifyModel


class EmailSettings(BaseModel):
    content: Optional[str]
    from_email: Optional[str] = 'airdrops@versifylabs.com'
    from_image: Optional[str]
    from_name: Optional[str]
    preview_text: Optional[str]
    subject_line: Optional[str]


class Recipients(BaseModel):
    count: int = 0
    segment_options: dict = {'conditions': '',  'match': 'all'}


class Airdrop(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'airdrop'
    created: int
    email_settings: Optional[EmailSettings]
    metadata: Optional[dict] = {}
    name: str = 'Unnamed Airdrop'
    product: str
    recipients: Optional[Recipients]
    status: str = 'draft'  # changes to sending -> complete
    updated: Optional[int]
