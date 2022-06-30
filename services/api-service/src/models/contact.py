from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Contact(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'contact'
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    created: int
    currency: str = 'usd'
    description: Optional[str]
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    organization: str
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'versify'
    tags: list = []
