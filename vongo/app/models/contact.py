from typing import List, Union

from pydantic import Field, HttpUrl

from .base import BaseCreate, BaseDoc, BaseUpdate
from .enums import ContactStatus
from .factory import contact_id, current_timestamp
from .globals import Location, PersonName, SocialProfile


class Contact(BaseDoc):
    """A contact document in the database."""

    __db__ = "Dev"
    __collection__ = "Contacts"

    id: str = Field(
        alias="_id",
        default_factory=contact_id,
        description="Unique identifier for the contact",
        example="cont_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    object: str = Field(
        default="contact",
        description="The object type. Always 'contact'",
        example="contact",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the contact belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
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
    name: PersonName = Field(
        default=None,
        description="The name of the contact. Includes first, middle and last name.",
        title="Name",
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


class ContactCreate(BaseCreate):
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


class ContactUpdate(BaseUpdate):
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
