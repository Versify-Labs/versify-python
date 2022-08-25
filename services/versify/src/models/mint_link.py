from typing import List, Optional

from pydantic import BaseModel, Field

from ..interfaces.versify_model import BaseVersifyModel


class BrandingColor(BaseModel):
    background: Optional[str]
    button: Optional[str]


class Branding(BaseModel):
    colors: Optional[BrandingColor]
    icon: Optional[str]
    logo: Optional[str]
    name: Optional[str]


class MintSpot(BaseModel):
    email: str
    mints_available: Optional[int] = 1
    mints_reserved: Optional[int] = 0


class MintLink(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    branding: Optional[Branding]
    object: str = 'mint_link'
    active: bool = True
    airdrop: Optional[str]
    created: int
    metadata: Optional[dict] = {}
    mint_list: Optional[List[MintSpot]] = []
    mints_available: Optional[int] = 0
    mints_reserved: Optional[int] = 0
    name: Optional[str]
    product: str
    public_mint: bool = True
    url: str  # example: "https://mint.versifylabs.com/{id}"
    updated: Optional[int]
