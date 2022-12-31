from typing import List

from pydantic import Field

from .base import Base
from .enums import BlockchainType
from .factory import asset_id, current_timestamp


class Asset(Base):
    id: str = Field(
        alias="_id",
        default_factory=asset_id,
        description="Unique identifier for the asset",
        example="ast_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    object: str = Field(
        default="asset",
        description="The object type",
        example="asset",
        title="Object Type",
    )
    account: str = Field(
        default=None,
        description="The account the asset belongs to",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    active: bool = Field(
        default=True,
        description="Whether the asset is active",
        example=True,
        title="Active",
    )
    chain: BlockchainType = Field(
        default=BlockchainType.POLYGON,
        description="The blockchain the asset is on",
        example="polygon",
        title="Blockchain",
    )
    collection: str = Field(
        ...,
        description="The collection the asset belongs to",
        example="collection",
        title="Collection",
    )
    contract_address: str = Field(
        ...,
        description="The contract address of the asset",
        example="0x1234567890123456789012345678901234567890",
        title="Contract Address",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the asset was created",
        example=1601059200,
        title="Created Timestamp",
    )
    default: bool = Field(
        default=False,
        description="Whether the asset is the default for the account",
        example=False,
        title="Account Default",
    )
    description: str = Field(
        ...,
        description="The description of the asset",
        example="This is a description",
        title="Description",
    )
    image: str = Field(
        ...,
        description="The image of the asset",
        example="https://example.com/image.png",
        title="Image",
    )
    metadata: dict = Field(
        default={}, description="Arbitrary metadata for the asset", title="Metadata"
    )
    name: str = Field(
        ..., description="The name of the asset", example="Asset Name", title="Name"
    )
    properties: List[dict] = Field(
        default=[], description="The properties of the asset", title="Properties"
    )
    tags: List[str] = Field(
        default=[], description="The tags of the asset", title="Tags"
    )
    token_id: str = Field(
        ...,
        description="The token ID of the asset",
        example="1234567890123456789012345678901234567890123456789012345678901234",
        title="Token ID",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the asset was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
