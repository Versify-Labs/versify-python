from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.factory import current_timestamp, tag_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Tag(Base):
    id: str = Field(
        alias="_id",
        default_factory=tag_id,
        description="Unique identifier for the tag",
        example="tag_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Tag ID",
    )
    object: str = Field(
        default="tag",
        description='The object type. Always "tag"',
        example="tag",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the tag belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the tag was created",
        example=1601059200,
        title="Created Timestamp",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the tag",
        example={"key": "value"},
        title="Metadata",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the tag was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )


class TagCreateRequest(Base):
    """A tag create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the tag",
        example={"key": "value"},
        title="Metadata",
    )


class TagCreateResponse(Tag):
    """A tag create response body."""

    pass


class TagDeleteRequest:
    """A tag delete request body."""

    pass


class TagDeleteResponse(Base):
    """A tag delete response body."""

    id: str = Field(
        description="Unique identifier for the tag",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Tag ID",
    )
    object: str = Field(
        default="tag",
        description="The object type",
        example="tag",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the tag has been deleted",
        example=True,
        title="Deleted",
    )


class TagGetRequest:
    """A tag get request body."""

    pass


class TagGetResponse(Tag):
    """A tag get response body."""

    pass


class TagListRequest:
    """A tag list request body."""

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
            description="The number of tags to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class TagListResponse(Base):
    """A tag list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of tags returned",
        example=1,
        title="Count",
    )
    data: List[Tag] = Field(
        default=[],
        description="The list of tags that match the filters and pagination parameters.",
        title="Tags",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more tags to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/tags",
        description="The URL of the list request",
        example="/v1/tags",
        title="URL",
    )


class TagSearchRequest(Base):
    """A tag search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class TagSearchResponse(Base):
    """A tag search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of tags returned",
        example=1,
        title="Count",
    )
    data: List[Tag] = Field(
        default=[],
        description="The list of tags that match the filters and pagination parameters.",
        title="Tags",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more tags to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/tags/search",
        description="The URL of the search request",
        example="/v1/tags/search",
        title="URL",
    )


class TagUpdateRequest(Base):
    """A tag update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the tag",
        example={"key": "value"},
        title="Metadata",
    )


class TagUpdateResponse(Tag):
    """A tag update response body."""

    pass
