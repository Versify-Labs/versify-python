from typing import Optional

from pydantic import EmailStr, Field

from ..interfaces.versify_model import BaseVersifyModel


class Contact(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'contact'
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    created: int
    currency: str = 'usd'
    description: str = ''
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []
    updated: Optional[int]
    wallet_address: Optional[str]
    wallets: Optional[list] = []
