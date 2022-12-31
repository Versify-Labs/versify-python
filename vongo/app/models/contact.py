from typing import List, Set, Union

from pydantic import Field, root_validator

from .base import Base
from .factory import contact_id, current_timestamp
from .globals import PersonName


class Contact(Base):
    id: str = Field(
        alias="_id",
        default_factory=contact_id,
        description="Unique identifier for the contact",
        example="cont_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    account: Union[str, None] = Field(
        default=None,
        description="The account the contact belongs to",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    object: str = Field(
        default="contact",
        description="The object type",
        example="contact",
        title="Object Type",
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
    name: PersonName = Field(
        default=PersonName(), description="The name of the contact", title="Name"
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the contact",
        example="+1 555 555 5555",
        title="Phone Number",
    )
    tags: Set[str] = Field(
        default=set(),
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


class ContactCreate(Base):
    email: str = Field(
        ...,
        description="The email address of the contact",
        example="jane@example.com",
        title="Email Address",
    )
    name: PersonName = Field(
        default=PersonName(), description="The name of the contact", title="Name"
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the contact",
        example="+1 555 555 5555",
        title="Phone Number",
    )
    tags: Union[Set[str], None] = Field(
        default=None,
        description="The tags associated with the contact",
        example=["tag1", "tag2"],
        title="Tags",
    )


class ContactUpdate(Base):
    name: Union[PersonName, None] = Field(
        default=None, description="The name of the contact", title="Name"
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the contact",
        example="+1 555 555 5555",
        title="Phone Number",
    )
    tags: Union[Set[str], None] = Field(
        default=None,
        description="The tags associated with the contact",
        example=["tag1", "tag2"],
        title="Tags",
    )


class ContactDeleted(Base):
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


class ContactList(Base):
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
        default=[], description="The list of contacts", title="Contacts"
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more contacts to be returned",
        example=False,
        title="Has More",
    )
