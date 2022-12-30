from typing import List, Sequence, Union

from pydantic import Field, root_validator

from .base import Base
from .factory import account_id, current_timestamp
from .globals import Billing, Brand, TeamMember


class AccountCreate(Base):
    name: str = Field(
        ...,
        description='The name of the account',
        example='Acme',
        title='Account Name'
    )


class AccountUpdate(Base):
    brand: Union[Brand, None] = Field(
        default=None,
        description='The brand of the account',
        title='Brand Settings'
    )
    domain: Union[str, None] = Field(
        default=None,
        description='The domain of the account',
        example='acme.com',
        title='Account Domain'
    )
    metadata: Union[dict, None] = Field(
        default=None,
        description='Arbitrary metadata for the account',
        title='Metadata'
    )
    name: Union[str, None] = Field(
        default=None,
        description='The name of the account',
        example='Acme Inc.',
        title='Account Name'
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the account was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )


class Account(Base):
    id: str = Field(
        alias="_id",
        default_factory=account_id,
        description='Unique identifier for the account',
        example='acct_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Account ID'
    )
    object: str = Field(
        default='account',
        description='The object type',
        example='account',
        title='Object Type'
    )
    billing: Billing = Field(
        default=Billing(),
        description='The billing settings of the account',
        title='Billing Settings'
    )
    brand: Brand = Field(
        default=Brand(),
        description='The branding settings of the account',
        title='Branding Settings'
    )
    created: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the account was created',
        example=1601059200,
        title='Created Timestamp'
    )
    domain: str = Field(
        ...,
        description='The domain of the account',
        example='acme.com',
        title='Account Domain'
    )
    metadata: dict = Field(
        default={},
        description='Arbitrary metadata for the account',
        title='Metadata'
    )
    name: str = Field(
        ...,
        description='The name of the account',
        example='Acme Inc.',
        title='Account Name'
    )
    team: List[TeamMember] = Field(
        default=[],
        description='The team members of the account',
        title='Team Members'
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the account was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )

    @root_validator(pre=True)
    def create_default_fields(cls, values):
        if not values.get('domain'):
            team = values.get('team', [])
            for member in team:
                email = member.get('email', '')
                if email:
                    domain = email.split('@')[1]
                    values['domain'] = domain
                    break
        return values


class AccountDeleteResult(Base):
    id: str = Field(
        description='Unique identifier for the account',
        example='acct_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Account ID'
    )
    object: str = Field(
        default='account',
        description='The object type',
        example='account',
        title='Object Type'
    )
    deleted: bool = Field(
        default=True,
        description='Whether the account has been deleted',
        example=True,
        title='Deleted'
    )


class AccountListResult(Base):
    object: str = Field(
        default='list',
        description='The object type',
        example='list',
        title='Object Type'
    )
    count: int = Field(
        default=0,
        description='The number of accounts returned',
        example=1,
        title='Count'
    )
    data: List[Account] = Field(
        default=[],
        description='The list of accounts',
        title='Accounts'
    )
    has_more: bool = Field(
        default=False,
        description='Whether there are more accounts to be returned',
        example=False,
        title='Has More'
    )


class AccountSearchResult(Base):
    results: Sequence[Account]
