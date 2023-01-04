from typing import List, Union

from app.models.base import Base
from app.models.enums import AssetStatus, BlockchainType
from app.models.factory import asset_id, current_timestamp
from app.models.globals import Note, Query
from fastapi import Query as QueryParam
from pydantic import Field, HttpUrl, validator


class Asset(Base):
    """A asset document in the database."""

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
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the asset was created",
        example=1601059200,
        title="Created Timestamp",
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
    metadata: dict = Field(
        default={},
        description="Arbitrary metadata associated with the asset",
        example={"key": "value"},
        title="Metadata",
    )
    name: str = Field(
        ...,
        description="The name of the asset. Displayed on third party apps.",
        example="Asset Name",
        title="Name",
    )
    notes: list[Note] = Field(
        default=[],
        description="The notes associated with the asset",
        title="Notes",
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
    tags: list[str] = Field(
        default=[],
        description="The tags associated with the asset",
        example=["tag1", "tag2"],
        title="Tags",
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

    @validator("tags")
    def tags_must_be_unique(cls, v):
        return list(set(v))


class AssetCreateRequest(Base):
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
    tags: list[str] = Field(
        default=[],
        description="The tags associated with the asset",
        example=["tag1", "tag2"],
        title="Tags",
    )


class AssetCreateResponse(Asset):
    """A asset create response body."""

    pass


class AssetDeleteRequest:
    """A asset delete request body."""

    pass


class AssetDeleteResponse(Base):
    """A asset delete response body."""

    id: str = Field(
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
    deleted: bool = Field(
        default=True,
        description="Whether the asset has been deleted",
        example=True,
        title="Deleted",
    )


class AssetGetRequest:
    """A asset get request body."""

    pass


class AssetGetResponse(Asset):
    """A asset get response body."""

    pass


class AssetListRequest:
    """A asset list request body."""

    def __init__(
        self,
        page_num: int = QueryParam(
            default=1,
            description="The page number to return",
            example=1,
            title="Page Number",
        ),
        page_size: int = QueryParam(
            default=20,
            description="The number of assets to return",
            example=20,
            title="Page Size",
        ),
        collection: str = QueryParam(
            default=None,
            description="The ID of the collection that the asset belongs to",
            example="collection",
            title="Collection",
        ),
        status: AssetStatus = QueryParam(
            default=AssetStatus.ACTIVE,
            description="The status of the asset",
            example=AssetStatus.ACTIVE,
            title="Status",
        ),
        tags: Union[List[str], None] = QueryParam(
            default=None,
            description="The tags associated with the asset",
            example=["tag1", "tag2"],
            title="Tags",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size
        self.collection = collection
        self.status = status
        self.tags = tags


class AssetListResponse(Base):
    """A asset list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of assets returned",
        example=1,
        title="Count",
    )
    data: List[Asset] = Field(
        default=[],
        description="The list of assets that match the filters and pagination parameters.",
        title="Assets",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more assets to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/assets",
        description="The URL of the list request",
        example="/v1/assets",
        title="URL",
    )


class AssetSearchRequest(Base):
    """A asset search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class AssetSearchResponse(Base):
    """A asset search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of assets returned",
        example=1,
        title="Count",
    )
    data: List[Asset] = Field(
        default=[],
        description="The list of assets that match the filters and pagination parameters.",
        title="Assets",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more assets to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/assets/search",
        description="The URL of the search request",
        example="/v1/assets/search",
        title="URL",
    )


class AssetUpdateRequest(Base):
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
    metadata: Union[dict, None] = Field(
        default=None,
        description="Arbitrary metadata associated with the asset",
        example={"key": "value"},
        title="Metadata",
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
    tags: Union[List[str], None] = Field(
        default=None,
        description="The tags associated with the asset",
        example=["tag1", "tag2"],
        title="Tags",
    )


class AssetUpdateResponse(Asset):
    """A asset update response body."""

    pass
