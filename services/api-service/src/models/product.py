from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Product(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: Optional[str]
    object: str = 'product'
    active: bool = True
    chain: Optional[str] = 'polygon'
    collection: str
    contract_address: Optional[str]
    created: int
    creator_avatar: Optional[str]
    creator_name: Optional[str]
    description: Optional[str]
    image: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    properties: list = []
    tags: list = []
    token_id: Optional[str]
    updated: Optional[int]
