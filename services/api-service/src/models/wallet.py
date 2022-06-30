from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class WalletAccount:
    address: str
    blockchain: str
    display_name: str = 'Wallet Account'


class Wallet(BaseVersifyModel):
    id: Optional[str] = Field(None, alias='_id')
    object: str = 'wallet'
    accounts: list = []
    created: int
    email: str
    metadata: Optional[dict] = {}
