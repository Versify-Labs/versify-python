from typing import Optional

from pydantic import Field

from ..interfaces.versify_model import BaseVersifyModel


class Collection(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'collection'
    active: bool = True
    # address of deployed contract
    contract_address: Optional[str]
    created: int
    default: Optional[bool] = False
    description: Optional[str] = 'Default collection'
    image: Optional[str] = 'https://cdn.versifylabs.com/branding/Logos/verisify-logo-transparent-bg.png'
    metadata: Optional[dict] = {}
    name: Optional[str] = 'Default collection'
    signature: Optional[str]
    # updates to pending, then failed or deployed once we receive transaction result
    status: str = 'new'
    tags: list = []
    transaction: Optional[str]
    updated: Optional[int]
    # in s3 bucket that has subfolder for each token_id: https:://s3.aws.{bucket_name}}/{contract_uri}/
    uri: Optional[str]
