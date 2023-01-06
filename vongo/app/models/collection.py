from typing import Union

from pydantic import Field

from ..core.constants import DEFAULT_LOGO
from .base import BaseCreate, BaseDoc, BaseUpdate
from .enums import CollectionStatus
from .factory import collection_id


class Collection(BaseDoc):
    """A collection document in the database."""

    __db__ = "Dev"
    __collection__ = "Collections"

    id: str = Field(
        alias="_id",
        default_factory=collection_id,
        description="Unique identifier for the collection",
        example="clm_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="User ID",
    )
    object: str = Field(
        default="collection",
        description='The object type. Always "collection"',
        example="collection",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the collection belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    status: str = Field(
        default=CollectionStatus.NEW,
        description="The status of the collection",
        example=CollectionStatus.NEW,
        title="Status",
    )
    contract_address: Union[str, None] = Field(
        default=None,
        description="The address of the contract",
        example="0x5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contract Address",
    )
    default: bool = Field(
        default=False,
        description="Whether this is the default collection",
        example=False,
        title="Default",
    )
    description: Union[str, None] = Field(
        default=None,
        description="The description of the collection",
        example="This is a collection",
        title="Description",
    )
    image: Union[str, None] = Field(
        default=DEFAULT_LOGO,
        description="The image of the collection",
        example="https://example.com/image.png",
        title="Image",
    )
    name: str = Field(
        ...,
        description="The name of the collection",
        example="Collection",
        title="Name",
    )
    signature: Union[str, None] = Field(
        default=None,
        description="The signature of the collection",
        example="0x5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Signature",
    )
    transaction: Union[str, None] = Field(
        default=None,
        description="The transaction of the collection",
        example="0x5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Transaction",
    )
    uri: Union[str, None] = Field(
        default=None,
        description="The uri of the collection",
        example="https://example.com",
        title="URI",
    )


class CollectionCreate(BaseCreate):
    """A collection create request body."""

    pass


class CollectionUpdate(BaseUpdate):
    """A collection update request body."""

    pass
