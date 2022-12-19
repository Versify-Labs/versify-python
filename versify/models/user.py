from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from ._base import BaseVersifyModel


class BlockchainWalletType(str, Enum):
    ethereum = "ethereum"
    bitcoin = "bitcoin"
    bsc = "bsc"
    solana = "solana"


class Wallet(BaseModel):
    """Information about a wallet that belongs to a Versify account/user"""
    address: str
    managed: bool = False
    type: BlockchainWalletType = BlockchainWalletType.ethereum


class User(BaseVersifyModel):
    """A user that belongs to a Versify organization"""
    object: str = 'user'
    active: bool = True
    avatar: Optional[str]
    email: EmailStr
    first_name: Optional[str]
    last_login: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    stytch_user: Optional[str]
    wallets: List[Wallet] = []
