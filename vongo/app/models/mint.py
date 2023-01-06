from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.enums import MintStatus
from app.models.factory import current_timestamp, mint_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import EmailStr, Field


class Mint(Base):
    id: str = Field(
        alias="_id",
        default_factory=mint_id,
        description="Unique identifier for the mint",
        example="mint_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Mint ID",
    )
    object: str = Field(
        default="mint",
        description='The object type. Always "mint"',
        example="mint",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the mint belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    asset: str = Field(
        ...,
        description="The asset the mint is for",
        example="asset_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the mint was created",
        example=1601059200,
        title="Created Timestamp",
    )
    contact: Union[str, None] = Field(
        default=None,
        description="The contact the mint is for",
        example="contact_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    email: Union[EmailStr, None] = Field(
        default=None, description="The email the mint is for", title="Email"
    )
    journey: Union[str, None] = Field(
        default=None, description="The journey the mint is for", title="Journey ID"
    )
    run: Union[str, None] = Field(
        default=None,
        description="The journey run the mint is for",
        title="Journey Run ID",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the mint",
        example={"key": "value"},
        title="Metadata",
    )
    quantity: int = Field(
        default=1, description="The quantity of the mint", example=1, title="Quantity"
    )
    signature: Union[str, None] = Field(
        default=None,
        description="The signature for the mint",
        example="signature",
        title="Signature",
    )
    status: MintStatus = Field(
        default=MintStatus.RESERVED,
        description="The status of the mint",
        example=MintStatus.RESERVED,
        title="Status",
    )
    transaction: Union[str, None] = Field(
        default=None,
        description="The transaction the mint is for",
        title="Transaction ID",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the mint was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
    wallet_address: Union[str, None] = Field(
        default=None,
        description="The wallet address the mint is for",
        title="Wallet Address",
    )


class MintCreateRequest(Base):
    """A mint create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the mint",
        example={"key": "value"},
        title="Metadata",
    )


class MintCreateResponse(Mint):
    """A mint create response body."""

    pass


class MintDeleteRequest:
    """A mint delete request body."""

    pass


class MintDeleteResponse(Base):
    """A mint delete response body."""

    id: str = Field(
        description="Unique identifier for the mint",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Mint ID",
    )
    object: str = Field(
        default="mint",
        description="The object type",
        example="mint",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the mint has been deleted",
        example=True,
        title="Deleted",
    )


class MintGetRequest:
    """A mint get request body."""

    pass


class MintGetResponse(Mint):
    """A mint get response body."""

    pass


class MintListRequest:
    """A mint list request body."""

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
            description="The number of mints to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class MintListResponse(Base):
    """A mint list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of mints returned",
        example=1,
        title="Count",
    )
    data: List[Mint] = Field(
        default=[],
        description="The list of mints that match the filters and pagination parameters.",
        title="Mints",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more mints to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/mints",
        description="The URL of the list request",
        example="/v1/mints",
        title="URL",
    )


class MintSearchRequest(Base):
    """A mint search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class MintSearchResponse(Base):
    """A mint search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of mints returned",
        example=1,
        title="Count",
    )
    data: List[Mint] = Field(
        default=[],
        description="The list of mints that match the filters and pagination parameters.",
        title="Mints",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more mints to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/mints/search",
        description="The URL of the search request",
        example="/v1/mints/search",
        title="URL",
    )


class MintUpdateRequest(Base):
    """A mint update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the mint",
        example={"key": "value"},
        title="Metadata",
    )


class MintUpdateResponse(Mint):
    """A mint update response body."""

    pass
