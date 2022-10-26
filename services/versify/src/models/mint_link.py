from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..interfaces.versify_model import BaseVersifyModel


class FontEnum(str, Enum):
    inherit = "inherit"


class ShapeEnum(str, Enum):
    rounded = "rounded"
    sharp = "sharp"
    pill = "pill"


class Branding(BaseModel):
    background_color: Optional[str] = "E1E4FF"  # type: ignore
    button_color: Optional[str] = "#596AFF"  # type: ignore
    font: Optional[FontEnum] = "inherit"  # type: ignore
    icon: Optional[str]
    logo: Optional[str]
    name: Optional[str]
    shapes: Optional[ShapeEnum] = "rounded"  # type: ignore


class MintSpot(BaseModel):
    email: EmailStr
    mints_available: Optional[int] = 1
    mints_reserved: Optional[int] = 0


class ReferenceIdCollection(BaseModel):
    enabled: bool = False
    label: Optional[str] = 'Reference ID'


class TaxIdCollection(BaseModel):
    enabled: bool = False
    label: Optional[str] = 'Tax ID'


class MintLink(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'mint_link'
    active: bool = True
    archived: Optional[bool] = False
    airdrop: Optional[str]
    branding: Optional[Branding]
    created: int
    metadata: Optional[dict] = {}
    mint_list: Optional[List[MintSpot]] = []
    mints_available: Optional[int] = 0
    mints_reserved: Optional[int] = 0
    name: Optional[str]
    product: str
    public_mint: bool = True
    reference_id_collection: Optional[ReferenceIdCollection]
    tax_id_collection: Optional[TaxIdCollection]
    url: str  # example: "https://mint.versifylabs.com/{id}"
    updated: Optional[int]
