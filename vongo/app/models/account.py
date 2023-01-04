from typing import List, Union

from app.models.base import Base
from app.models.enums import AccountStatus
from app.models.factory import account_id, current_timestamp
from app.models.globals import Billing, Brand, Query, TeamMember
from fastapi import Query as QueryParam
from pydantic import Field, root_validator


class Account(Base):
    """A account document in the database."""

    id: str = Field(
        alias="_id",
        default_factory=account_id,
        description="Unique identifier for the account",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    object: str = Field(
        default="account",
        description="The object type",
        example="account",
        title="Object Type",
    )
    billing: Billing = Field(
        default=Billing(),
        description="The billing settings of the account",
        title="Billing Settings",
    )
    brand: Brand = Field(
        default=Brand(),
        description="The branding settings of the account",
        title="Branding Settings",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the account was created",
        example=1601059200,
        title="Created Timestamp",
    )
    domain: str = Field(
        ...,
        description="The domain of the account",
        example="acme.com",
        title="Account Domain",
    )
    metadata: dict = Field(
        default={},
        description="Arbitrary metadata for the account. Can be used to store internal identifiers.",
        title="Metadata",
    )
    name: str = Field(
        ...,
        description="The name of the account",
        example="Acme Inc.",
        title="Account Name",
    )
    status: AccountStatus = Field(
        default=AccountStatus.ACTIVE,
        description="The status of the account",
        example=AccountStatus.ACTIVE,
        title="Account Status",
    )
    team: List[TeamMember] = Field(
        default=[],
        description="The team members and associated roles of the account",
        title="Team Members",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the account was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )

    @root_validator(pre=True)
    def create_default_fields(cls, values):
        if not values.get("domain"):
            team = values.get("team", [])
            for member in team:
                email = member.get("email", "")
                if email:
                    domain = email.split("@")[1]
                    values["domain"] = domain
                    break
        return values


class AccountCreateRequest(Base):
    """A account create request body."""

    name: str = Field(
        ...,
        description="The name of the account. Displayable to customers.",
        example="Acme",
        title="Name",
    )
    domain: Union[str, None] = Field(
        default=None,
        description="The domain of the account. Displayable to customers.",
        example="acme.com",
        title="Domain",
    )


class AccountCreateResponse(Account):
    """A account create response body."""

    pass


class AccountDeleteRequest:
    """A account delete request body."""

    pass


class AccountDeleteResponse(Base):
    """A account delete response body."""

    id: str = Field(
        description="Unique identifier for the account",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    object: str = Field(
        default="account",
        description="The object type",
        example="account",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the account has been deleted",
        example=True,
        title="Deleted",
    )


class AccountGetRequest:
    """A account get request body."""

    pass


class AccountGetResponse(Account):
    """A account get response body."""

    pass


class AccountListRequest:
    """A account list request body."""

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
            description="The number of accounts to return",
            example=20,
            title="Page Size",
        ),
        status: AccountStatus = QueryParam(
            default=AccountStatus.ACTIVE,
            description="The status of the account",
            example=AccountStatus.ACTIVE,
            title="Status",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size
        self.status = status


class AccountListResponse(Base):
    """A account list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of accounts returned",
        example=1,
        title="Count",
    )
    data: List[Account] = Field(
        default=[],
        description="The list of accounts that match the filters and pagination parameters.",
        title="Accounts",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more accounts to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/accounts",
        description="The URL of the list request",
        example="/v1/accounts",
        title="URL",
    )


class AccountSearchRequest(Base):
    """A account search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class AccountSearchResponse(Base):
    """A account search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of accounts returned",
        example=1,
        title="Count",
    )
    data: List[Account] = Field(
        default=[],
        description="The list of accounts that match the filters and pagination parameters.",
        title="Accounts",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more accounts to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/accounts/search",
        description="The URL of the search request",
        example="/v1/accounts/search",
        title="URL",
    )


class AccountUpdateRequest(Base):
    """A account update request body."""

    brand: Union[Brand, None] = Field(
        default=None,
        description="The brand settings for the account",
        title="Brand Settings",
    )
    domain: Union[str, None] = Field(
        default=None,
        description="The domain of the account",
        example="acme.com",
        title="Account Domain",
    )
    metadata: Union[dict, None] = Field(
        default=None, description="Arbitrary metadata for the account", title="Metadata"
    )
    name: Union[str, None] = Field(
        default=None,
        description="The name of the account",
        example="Acme Inc.",
        title="Account Name",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the account was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )


class AccountUpdateResponse(Account):
    """A account update response body."""

    pass
