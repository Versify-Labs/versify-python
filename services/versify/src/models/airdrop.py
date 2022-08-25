from typing import Optional

from pydantic import BaseModel, Field

from ..interfaces.versify_model import BaseVersifyModel


class EmailSettings(BaseModel):
    content: Optional[str] = 'Claim your free NFT.'
    from_email: Optional[str] = 'airdrops@versifylabs.com'
    from_image: Optional[str]
    from_name: Optional[str] = 'Versify Labs'
    preview_text: Optional[str] = 'Claim your free NFT'
    subject_line: Optional[str] = 'Claim your free NFT'


class Recipients(BaseModel):
    count: int = 0
    segment_options: dict = {'conditions': '',  'match': 'all'}
    emails_included: Optional[list] = []
    emails_excluded: Optional[list] = []
    tags_included: Optional[list] = []
    tags_excluded: Optional[list] = []


class Airdrop(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'airdrop'
    created: int
    email_settings: Optional[EmailSettings]
    metadata: Optional[dict] = {}
    mint_link: Optional[str]
    name: str = 'Unnamed Airdrop'
    product: str
    recipients: Optional[Recipients]
    status: str = 'draft'  # changes to sending -> complete
    updated: Optional[int]
