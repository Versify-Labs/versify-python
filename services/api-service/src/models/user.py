from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class User(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'user'
    active: bool = True
    avatar: Optional[str]
    created: int
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    phone: Optional[str]
    stytch_user: Optional[str]
    updated: int
    wallets: list = []
