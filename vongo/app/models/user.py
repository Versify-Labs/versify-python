from typing import List, Union

from pydantic import EmailStr, Field, root_validator

from .base import BaseDoc, BaseUpdate
from .factory import generate_avatar, user_id
from .globals import IdentityProvider, PersonName


class User(BaseDoc):
    """A user document in the database."""

    __db__ = "Dev"
    __collection__ = "Users"

    id: str = Field(
        alias="_id",
        default_factory=user_id,
        description="Unique identifier for the user",
        example="user_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="User ID",
    )
    object: str = Field(
        default="user",
        description='The object type. Always "user"',
        example="user",
        title="Object Type",
    )
    active: bool = Field(
        default=True,
        description="Whether the user is active",
        example=True,
        title="Active",
    )
    avatar: str = Field(
        ...,
        description="The URL of the user's avatar",
        example="https://example.com/avatar.png",
        title="Avatar URL",
    )
    email: EmailStr = Field(
        ...,
        description="The email address of the user",
        example="jane@example.com",
        title="Email Address",
    )
    email_verified: bool = Field(
        default=False,
        description="Whether the user's email address has been verified",
        example=True,
        title="Email Verified",
    )
    name: PersonName = Field(
        default=PersonName(), description="The name of the user", title="Name"
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the user",
        example="+15555555555",
        title="Phone Number",
    )
    phone_number_verified: bool = Field(
        default=False,
        description="Whether the user's phone number has been verified",
        example=True,
        title="Phone Number Verified",
    )
    providers: List[IdentityProvider] = Field(
        default=[],
        description="The identity providers the user belongs to",
        title="Identity Providers",
    )

    @root_validator(pre=True)
    def default_values(cls, values):
        values["email"] = values["email"].lower()
        if "avatar" not in values:
            values["avatar"] = generate_avatar(values["email"])
        return values


class UserUpdate(BaseUpdate):
    """A user update ressponse body."""

    avatar: Union[str, None] = Field(
        default=None,
        description="The URL of the user's avatar",
        example="https://example.com/avatar.png",
        title="Avatar URL",
    )
    name: Union[PersonName, None] = Field(
        default=None, description="The name of the user", title="Name"
    )
    phone_number: Union[str, None] = Field(
        default=None,
        description="The phone number of the user",
        example="+15555555555",
        title="Phone Number",
    )
