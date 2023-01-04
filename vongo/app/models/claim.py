from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.enums import ClaimStatus
from app.models.factory import claim_id, current_timestamp
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Claim(Base):
    """A claim document in the database."""

    id: str = Field(
        alias="_id",
        default_factory=claim_id,
        description="Unique identifier for the claim",
        example="clm_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="User ID",
    )
    object: str = Field(
        default="claim",
        description='The object type. Always "claim"',
        example="claim",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the claim belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    asset: str = Field(
        ...,
        description="The asset being claimed",
        example="asset_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the claim was created",
        example=16,
    )
    code: str = Field(
        ...,
        description="The code used to submit the claim.",
        example="ABC123",
        title="Code",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the claim",
        example={"key": "value"},
        title="Metadata",
    )
    quantity: int = Field(
        default=1,
        description="The number of assets being claimed",
        example=1,
        title="Quantity",
    )
    status: str = Field(
        default=ClaimStatus.REQUESTED,
        description="The status of the claim",
        example=ClaimStatus.REQUESTED,
        title="Status",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the user was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )


class ClaimCreateRequest(Base):
    """A claim create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the claim",
        example={"key": "value"},
        title="Metadata",
    )


class ClaimCreateResponse(Claim):
    """A claim create response body."""

    pass


class ClaimDeleteRequest:
    """A claim delete request body."""

    pass


class ClaimDeleteResponse(Base):
    """A claim delete response body."""

    id: str = Field(
        description="Unique identifier for the claim",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Claim ID",
    )
    object: str = Field(
        default="claim",
        description="The object type",
        example="claim",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the claim has been deleted",
        example=True,
        title="Deleted",
    )


class ClaimGetRequest:
    """A claim get request body."""

    pass


class ClaimGetResponse(Claim):
    """A claim get response body."""

    pass


class ClaimListRequest:
    """A claim list request body."""

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
            description="The number of claims to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class ClaimListResponse(Base):
    """A claim list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of claims returned",
        example=1,
        title="Count",
    )
    data: List[Claim] = Field(
        default=[],
        description="The list of claims that match the filters and pagination parameters.",
        title="Claims",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more claims to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/claims",
        description="The URL of the list request",
        example="/v1/claims",
        title="URL",
    )


class ClaimSearchRequest(Base):
    """A claim search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class ClaimSearchResponse(Base):
    """A claim search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of claims returned",
        example=1,
        title="Count",
    )
    data: List[Claim] = Field(
        default=[],
        description="The list of claims that match the filters and pagination parameters.",
        title="Claims",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more claims to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/claims/search",
        description="The URL of the search request",
        example="/v1/claims/search",
        title="URL",
    )


class ClaimUpdateRequest(Base):
    """A claim update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the claim",
        example={"key": "value"},
        title="Metadata",
    )


class ClaimUpdateResponse(Claim):
    """A claim update response body."""

    pass
