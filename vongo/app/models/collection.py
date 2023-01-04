from typing import Optional

from app.core.constants import DEFAULT_LOGO
from app.models.base import Base
from app.models.enums import CollectionStatus


class Collection(Base):
    object: str = "collection"
    active: bool = True
    contract_address: Optional[str]
    default: Optional[bool] = False
    description: Optional[str] = "Default collection"
    image: Optional[str] = DEFAULT_LOGO
    name: str = ""
    signature: Optional[str]
    status: CollectionStatus = CollectionStatus.NEW
    tags: list = []
    transaction: Optional[str]
    # in s3 bucket that has subfolder for each token_id: https:://s3.aws.{bucket_name}}/{contract_uri}/
    uri: Optional[str]
