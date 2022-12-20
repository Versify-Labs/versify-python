from typing import Optional

from pydantic import BaseModel, EmailStr

from ._base import BaseAccountModel


class Note(BaseModel):
    id: str
    object = 'note'
    created: int
    content: str = ''
    user: dict = {}


class Contact(BaseAccountModel):
    object = 'contact'
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
    notes: list[Note] = []
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []
    wallet_address: Optional[str]
