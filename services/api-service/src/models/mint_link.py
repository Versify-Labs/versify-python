from typing import Optional

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


class MintLink(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    branding: Optional[Branding]
    object: str = 'mint_link'
    active: bool = True
    created: int
    metadata: Optional[dict] = {}
    product: str
    public_mint: bool = True
    url: str  # example: "https://mint.versifylabs.com/{id}"
    updated: Optional[int]
