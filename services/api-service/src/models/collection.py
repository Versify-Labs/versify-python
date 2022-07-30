from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Collection(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: Optional[str]
    object: str = 'collection'
    active: bool = True
    # address of deployed contract
    contract_address: Optional[str]
    created: int
    description: Optional[str]
    image: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    signature: Optional[str]
    # updates to pending, then failed or deployed once we receive transaction result
    status: str = 'new'
    tags: list = []
    transaction: Optional[str]
    updated: Optional[int]
    # in s3 bucket that has subfolder for each token_id: https:://s3.aws.{bucket_name}}/{contract_uri}/
    uri: Optional[str]
