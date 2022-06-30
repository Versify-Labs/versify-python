from typing import Optional

from pydantic import Field

from .base import BaseCampaign


class MintLink(BaseCampaign):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'mint_link'

    active: bool = True
    created: int
    metadata: Optional[dict] = {}
    organization: Optional[str]
    product: str
    url: str  # example: "https://mint.versifylabs.com/{id}"
