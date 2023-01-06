from typing import Optional

from ._base import BaseAccountModel


class Product(BaseAccountModel):
    """Product model."""

    object: str = "product"
    active: bool = True
    chain: Optional[str] = "polygon"
    collection: str
    contract_address: Optional[str]
    creator_avatar: Optional[str]
    creator_name: Optional[str]
    default: bool = False
    description: Optional[str]
    image: Optional[str]
    name: Optional[str]
    properties: list = []
    tags: list = []
    token_id: Optional[str]
