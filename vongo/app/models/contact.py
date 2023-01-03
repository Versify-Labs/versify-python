from typing import List, Union

from app.models.base import Base
from app.models.enums import ContactStatus
from app.models.factory import contact_id, current_timestamp
from app.models.globals import Location, Note, PersonName, Query, SocialProfile
from fastapi import Query as QueryParam
from pydantic import Field, HttpUrl, validator


class Contact(Base):
    """A contact document in the database."""

    id: str = Field(
        alias="_id",
        default_factory=contact_id,
        description="Unique identifier for the contact",
        example="cont_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    object: str = Field(
        default="contact",
        description="The object type",
        example="contact",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the contact belongs to",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    avatar: HttpUrl = Field(
        default=None,
        description="The URL of the contact's avatar",
        example="https://example.com/avatar.png",
        title="Avatar URL",
    )
    browser: str = Field(
        default=None,
        description="The browser used by the contact",
        example="Chrome",
        title="Browser",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the contact was created",
        example=1601059200,
        title="Created Timestamp",
    )
    email: str = Field(
        ...,
        description="The email address of the contact",
        example="jane@example.com",
        title="Email Address",
    )
    last_seen: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the contact was last seen",
        example=1601059200,
        title="Last Seen Timestamp",
    )
    location: Location = Field(
        default=None,
        description="The location of the contact",
        title="Location",
    )
    metadata: dict = Field(
        default={},
        description="Arbitrary metadata associated with the contact",
        example={"key": "value"},
        title="Metadata",
    )
    name: PersonName = Field(
        default=None,
        description="The name of the contact. Includes first, middle and last name.",
        title="Name",
    )
    notes: list[Note] = Field(
        default=[],
        description="The notes associated with the contact",
        title="Notes",
    )
    owner: str = Field(
        default=None,
        description="The ID of the user who owns the contact",
        example="user_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Owner ID",
    )
    phone_number: str = Field(
        default=None,
        description="The phone number of the contact",
        example="+1 555 555 5555",
        title="Phone Number",
    )
    social_profiles: List[SocialProfile] = Field(
        default=[],
        description="The social profiles associated with the contact",
        title="Social Profiles",
    )
    status: ContactStatus = Field(
        default=ContactStatus.ACTIVE,
        description="The status of the contact",
        example=ContactStatus.ACTIVE,
        title="Status",
    )
    tags: list[str] = Field(
        default=[],
        description="The tags associated with the contact",
        example=["tag1", "tag2"],
        title="Tags",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the contact was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )

    @validator("tags")
    def tags_must_be_unique(cls, v):
        return list(set(v))


class ContactCreateRequest(Base):
    """A contact create request body."""

    email: str = Field(
        ...,
        description="The email address of the contact",
        example="jane@example.com",
        title="Email Address",
    )
    name: Union[PersonName, None] = Field(
        default=PersonName(),
        description="The name of the contact. Can include first, middle, and/or last name.",
        title="Name",
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the contact",
        example="+1 555 555 5555",
        title="Phone Number",
    )
    tags: Union[set[str], None] = Field(
        default=set(),
        description="The tags associated with the contact",
        example=["tag1", "tag2"],
        title="Tags",
    )


class ContactCreateResponse(Contact):
    """A contact create response body."""

    pass


class ContactDeleteRequest:
    """A contact delete request body."""

    pass


class ContactDeleteResponse(Base):
    """A contact delete response body."""

    id: str = Field(
        description="Unique identifier for the contact",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    object: str = Field(
        default="contact",
        description="The object type",
        example="contact",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the contact has been deleted",
        example=True,
        title="Deleted",
    )


class ContactGetRequest:
    """A contact get request body."""

    pass


class ContactGetResponse(Contact):
    """A contact get response body."""

    pass


class ContactListRequest:
    """A contact list request body."""

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
            description="The number of contacts to return",
            example=20,
            title="Page Size",
        ),
        owner: Union[str, None] = QueryParam(
            default=None,
            description="The ID of the user who owns the contact",
            title="Owner ID",
        ),
        status: ContactStatus = QueryParam(
            default=ContactStatus.ACTIVE,
            description="The status of the contact",
            example=ContactStatus.ACTIVE,
            title="Status",
        ),
        tags: Union[List[str], None] = QueryParam(
            default=None,
            description="The tags associated with the contact",
            example=["tag1", "tag2"],
            title="Tags",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size
        self.owner = owner
        self.status = status
        self.tags = tags


class ContactListResponse(Base):
    """A contact list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of contacts returned",
        example=1,
        title="Count",
    )
    data: List[Contact] = Field(
        default=[],
        description="The list of contacts that match the filters and pagination parameters.",
        title="Contacts",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more contacts to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/contacts",
        description="The URL of the list request",
        example="/v1/contacts",
        title="URL",
    )


class ContactSearchRequest(Base):
    """A contact search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class ContactSearchResponse(Base):
    """A contact search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of contacts returned",
        example=1,
        title="Count",
    )
    data: List[Contact] = Field(
        default=[],
        description="The list of contacts that match the filters and pagination parameters.",
        title="Contacts",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more contacts to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/contacts/search",
        description="The URL of the search request",
        example="/v1/contacts/search",
        title="URL",
    )


class ContactUpdateRequest(Base):
    """A contact update request body."""

    name: Union[PersonName, None] = Field(
        default=None,
        description="The name of the contact. Can include first, middle, and/or last name.",
        title="Name",
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the contact",
        example="+1 555 555 5555",
        title="Phone Number",
    )
    tags: Union[set[str], None] = Field(
        default=None,
        description="The tags associated with the contact",
        example=["tag1", "tag2"],
        title="Tags",
    )


class ContactUpdateResponse(Contact):
    """A contact update response body."""

    pass
