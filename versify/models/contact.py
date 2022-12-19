from typing import Optional

from pydantic import EmailStr

from ._base import BaseAccountModel


class Contact(BaseAccountModel):
    object: str = 'contact'
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    currency: str = 'usd'
    description: str = ''
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []
    wallet_address: Optional[str]
