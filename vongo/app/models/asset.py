from typing import List, Union

from pydantic import Field, HttpUrl

from .base import BaseCreate, BaseDoc, BaseUpdate
from .enums import AssetStatus, BlockchainType
from .factory import asset_id, current_timestamp


class Asset(BaseDoc):
    """A asset document in the database."""

    __db__ = "Dev"
    __collection__ = "Assets"

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
        ...,
        description="The account the asset belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    chain: BlockchainType = Field(
        default=BlockchainType.POLYGON,
        description="The blockchain the asset is on",
        example="polygon",
        title="Blockchain",
    )
    collection: str = Field(
        ...,
        description="The ID of the collection that the asset belongs to",
        example="col_1231231231231312312312313",
        title="Collection",
    )
    contract_address: str = Field(
        ...,
        description="The contract address of the asset",
        example="0x1234567890123456789012345678901234567890",
        title="Contract Address",
    )
    description: str = Field(
        ...,
        description="The description of the asset",
        example="This is a description",
        title="Description",
    )
    image: HttpUrl = Field(
        ...,
        description="The image of the asset",
        example="https://example.com/image.png",
        title="Image",
    )
    name: str = Field(
        ...,
        description="The name of the asset. Displayed on third party apps.",
        example="Asset Name",
        title="Name",
    )
    properties: List[dict] = Field(
        default=[],
        description="The properties of the asset. Displayed on third party apps.",
        title="Properties",
    )
    status: AssetStatus = Field(
        default=AssetStatus.ACTIVE,
        description="The status of the asset",
        example=AssetStatus.ACTIVE,
        title="Status",
    )
    token_id: str = Field(
        ...,
        description="The token ID of the asset",
        example="1234567890123456789012345678901234567890123456789012345678901234",
        title="Token ID",
    )


class AssetCreate(BaseCreate):
    """A asset create request body."""

    description: str = Field(
        ...,
        description="The description of the asset",
        example="This is a description",
        title="Description",
    )
    image: HttpUrl = Field(
        ...,
        description="The image of the asset",
        example="https://example.com/image.png",
        title="Image",
    )
    name: str = Field(
        ...,
        description="The name of the asset. Displayed on third party apps.",
        example="Asset Name",
        title="Name",
    )
    properties: List[dict] = Field(
        default=[],
        description="The properties of the asset. Displayed on third party apps.",
        title="Properties",
    )


class AssetUpdate(BaseUpdate):
    """A asset update request body."""

    description: Union[str, None] = Field(
        default=None,
        description="The description of the asset",
        example="This is a description",
        title="Description",
    )
    image: Union[HttpUrl, None] = Field(
        default=None,
        description="The image of the asset",
        example="https://example.com/image.png",
        title="Image",
    )
    name: Union[str, None] = Field(
        default=None,
        description="The name of the asset. Displayed on third party apps.",
        example="Asset Name",
        title="Name",
    )
    properties: Union[List[dict], None] = Field(
        default=None,
        description="The properties of the asset. Displayed on third party apps.",
        title="Properties",
    )
    status: Union[AssetStatus, None] = Field(
        default=None,
        description="The status of the asset",
        example=AssetStatus.ACTIVE,
        title="Status",
    )
