from typing import List, Union

from pydantic import Field, root_validator

from .base import BaseCreate, BaseDoc, BaseUpdate
from .enums import AccountStatus
from .factory import account_id, generate_avatar
from .globals import App, Billing, Brand, TeamMember


class Account(BaseDoc):
    """A account document in the database."""

    __db__ = "Dev"
    __collection__ = "Accounts"

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
    apps: List[App] = Field(
        default=[],
        description="The apps associated with the account",
        title="Apps",
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
    domain: str = Field(
        ...,
        description="The domain of the account",
        example="acme.com",
        title="Account Domain",
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

    @root_validator(pre=True)
    def create_default_fields(cls, values):
        name = values.get("name", "Versify")
        if not values.get("brand"):
            values["brand"] = Brand(logo=generate_avatar(name))
        if not values.get("domain"):
            team = values.get("team", [])
            for member in team:
                email = member.get("email", "")
                if email:
                    domain = email.split("@")[1]
                    values["domain"] = domain
                    break
        return values


class AccountCreate(BaseCreate):
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


class AccountUpdate(BaseUpdate):
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
    name: Union[str, None] = Field(
        default=None,
        description="The name of the account",
        example="Acme Inc.",
        title="Account Name",
    )
