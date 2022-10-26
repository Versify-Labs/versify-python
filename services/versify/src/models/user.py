from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..interfaces.versify_model import BaseVersifyModel


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

    # Do not include this in the response
    # private_key: Optional[str]


class User(BaseVersifyModel):
    """A user that belongs to a Versify organization"""
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'user'
    active: bool = True
    avatar: Optional[str]
    created: int
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_login: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    phone: Optional[str]
    stytch_user: Optional[str]
    updated: int
    wallets: Optional[List[Wallet]] = []
