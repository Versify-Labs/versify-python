from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseVersifyModel


class BrandingColor(BaseModel):
    background: Optional[str]
    button: Optional[str]


class Branding(BaseModel):
    colors: Optional[BrandingColor]
    icon: Optional[str]
    logo: Optional[str]
    name: Optional[str]


class WhitelistSpot(BaseModel):
    email: str
    status: str = 'reserved'  # updates to claimed


class MintLink(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    branding: Optional[Branding]
    object: str = 'mint_link'
    active: bool = True
    airdrop: Optional[str]
    created: int
    metadata: Optional[dict] = {}
    name: Optional[str]
    product: str
    public_mint: bool = True
    url: str  # example: "https://mint.versifylabs.com/{id}"
    updated: Optional[int]
    whitelist: Optional[List[WhitelistSpot]] = []
