from typing import Any, Dict, List, Union

from app.core.constants import DEFAULT_LOGO
from app.models.base import Base
from app.models.enums import CollectionStatus
from app.models.factory import collection_id, current_timestamp
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Collection(Base):
    """A collection document in the database."""

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
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the collection was created",
        example=16,
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the collection",
        example={"key": "value"},
        title="Metadata",
    )
    status: str = Field(
        default=CollectionStatus.NEW,
        description="The status of the collection",
        example=CollectionStatus.NEW,
        title="Status",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the user was last updated",
        example=1601059200,
        title="Updated Timestamp",
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


class CollectionCreateRequest(Base):
    """A collection create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the collection",
        example={"key": "value"},
        title="Metadata",
    )


class CollectionCreateResponse(Collection):
    """A collection create response body."""

    pass


class CollectionDeleteRequest:
    """A collection delete request body."""

    pass


class CollectionDeleteResponse(Base):
    """A collection delete response body."""

    id: str = Field(
        description="Unique identifier for the collection",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Collection ID",
    )
    object: str = Field(
        default="collection",
        description="The object type",
        example="collection",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the collection has been deleted",
        example=True,
        title="Deleted",
    )


class CollectionGetRequest:
    """A collection get request body."""

    pass


class CollectionGetResponse(Collection):
    """A collection get response body."""

    pass


class CollectionListRequest:
    """A collection list request body."""

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
            description="The number of collections to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class CollectionListResponse(Base):
    """A collection list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of collections returned",
        example=1,
        title="Count",
    )
    data: List[Collection] = Field(
        default=[],
        description="The list of collections that match the filters and pagination parameters.",
        title="Collections",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more collections to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/collections",
        description="The URL of the list request",
        example="/v1/collections",
        title="URL",
    )


class CollectionSearchRequest(Base):
    """A collection search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class CollectionSearchResponse(Base):
    """A collection search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of collections returned",
        example=1,
        title="Count",
    )
    data: List[Collection] = Field(
        default=[],
        description="The list of collections that match the filters and pagination parameters.",
        title="Collections",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more collections to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/collections/search",
        description="The URL of the search request",
        example="/v1/collections/search",
        title="URL",
    )


class CollectionUpdateRequest(Base):
    """A collection update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the collection",
        example={"key": "value"},
        title="Metadata",
    )


class CollectionUpdateResponse(Collection):
    """A collection update response body."""

    pass
