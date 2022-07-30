from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseVersifyModel


class EmailSettings(BaseModel):
    content: Optional[str]
    from_email: Optional[str]
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

    # "body": {
    #     "email_settings": {
    #         "content": "Enjoy this complimentary NFT.",
    #         "from_email": "claims@versifylabs.com",
    #         "from_image": "https://uploads-ssl.webflow.com/61f99f3055f0fb37c1005252/61f99f3155f0fb4ba7005411_image-2-help-center-saas-x-template.svg",
    #         "from_name": "Acme Corp",
    #         "preview_text": "Complimentary NFT from Acme Corp",
    #         "subject_line": "Complimentary NFT from Acme Corp"
    #     },
    #     "name": "Jul 24 Airdrop",
    #     "product": "prod_62dded659aa81a9bb00da543"
    # },
