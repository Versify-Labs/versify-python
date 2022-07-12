from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Account(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'account'
    active: bool = True
    avatar: Optional[str]
    business_profile: Optional[dict] = {}
    business_type: Optional[str]
    company: Optional[dict] = {}
    country: str = 'US'
    created: int
    currency: str = 'usd'
    description: str = ''
    email: str
    individual: Optional[dict] = {}
    metadata: Optional[dict] = {}
    name: Optional[str]
    settings: Optional[dict] = {}
