import secrets
from typing import Optional, Union

from eth_account import Account as EthAccount
from pydantic import EmailStr, Field, HttpUrl, root_validator, validator

from .base import Base
from .enums import (ActionType, Operator, RunStatus, SubscriptionPlan,
                    SubscriptionStatus, TeamMemberRole, TriggerType,
                    WalletType)
from .factory import (api_public_key, api_secret_key,
                      generate_stripe_customer_id)


class Authentication(Base):
    """Settings used to configure how this account can be accessed"""
    api_public_key: str = Field(
        default_factory=api_public_key,
        description='The public key used to authenticate with the API',
        example='pk_123',
        title='API Public Key'
    )
    api_secret_key: str = Field(
        default_factory=api_secret_key,
        description='The secret key used to authenticate with the API',
        example='sk_123',
        title='API Secret Key'
    )


class Filter(Base):
    """URL pattern used to configure the account's brand"""
    field: str = Field(
        ...,
        description='The field to filter on',
        example='url',
        title='Field'
    )
    operator: Operator = Field(
        ...,
        description='The operator to use',
        example='contains',
        title='Operator'
    )
    value: str = Field(
        ...,
        description='The value to filter on',
        example='example.com',
        title='Value'
    )


class Image(Base):
    name: str = Field(
        ...,
        description='The name of the image',
        example='Logo',
        title='Image Name'
    )
    url: HttpUrl = Field(
        ...,
        description='The URL of the image',
        example='https://example.com/logo.png',
        title='Image URL'
    )


class Billing(Base):
    stripe_customer_id: str = Field(
        default_factory=generate_stripe_customer_id,
        description='The Stripe customer ID',
        example='cus_123',
        title='Stripe Customer ID'
    )
    subscription_plan: SubscriptionPlan = Field(
        default=SubscriptionPlan.TRIAL,
        description='The subscription plan',
        example='growth',
        title='Subscription Plan'
    )
    subscription_status: SubscriptionStatus = Field(
        default=SubscriptionStatus.ACTIVE,
        description='The subscription status',
        example='active',
        title='Subscription Status'
    )


class Brand(Base):
    logo: Union[Image, None] = Field(
        default=None,
        description='The logo of the brand',
        title='Logo'
    )
    action_color: Union[str, None] = Field(
        default=None,
        description='The action color of the brand',
        example='#000000',
        title='Action Color'
    )
    background_color: Union[str, None] = Field(
        default=None,
        description='The background color of the brand',
        example='#000000',
        title='Background Color'
    )
    primary_color: Union[str, None] = Field(
        default=None,
        description='The primary color of the brand',
        example='#000000',
        title='Primary Color'
    )
    secondary_color: Union[str, None] = Field(
        default=None,
        description='The secondary color of the brand',
        example='#000000',
        title='Secondary Color'
    )
    tertiary_color: Union[str, None] = Field(
        default=None,
        description='The tertiary color of the brand',
        example='#000000',
        title='Tertiary Color'
    )


class IdentityProvider(Base):
    provider_type: str = Field(
        ...,
        description='The type of the identity provider',
        example='google',
        title='Provider Type'
    )
    provider_subject: str = Field(
        ...,
        description='The subject of the identity provider',
        example='1234567890',
        title='Provider Subject'
    )


class Note(Base):
    id: str = Field(
        ...,
        description='The ID of the note',
        example='123',
        title='Note ID'
    )
    author: dict = Field(
        ...,
        description='The author of the note',
        example={'id': '123', 'name': 'Jane Doe'},
        title='Note Author'
    )
    created: int = Field(
        ...,
        description='The timestamp of when the note was created',
        example=1629023389,
        title='Created Timestamp'
    )
    content: str = Field(
        default='',
        description='The content of the note',
        example='This is a note',
        title='Note Content'
    )


class PersonName(Base):
    first_name: Union[str, None] = Field(
        default=None,
        description='The first name of the person',
        example='Jane',
        title='First Name'
    )
    middle_name: Union[str, None] = Field(
        default=None,
        description='The middle name of the person',
        example='M.',
        title='Middle Name'
    )
    last_name: Union[str, None] = Field(
        default=None,
        description='The last name of the person',
        example='Doe',
        title='Last Name'
    )

    @validator('first_name', 'middle_name', 'last_name', pre=True)
    def validate_names(cls, v):
        if v and v is not None and not v.isalpha():
            raise ValueError('Names must only contain letters')
        return v.title()


class TeamMember(Base):
    email: EmailStr = Field(
        ...,
        description='The email of the team member',
        example='jane@example.com',
        title='Email'
    )
    role: TeamMemberRole = Field(
        default=TeamMemberRole.MEMBER,
        description='The role of the team member',
        example='member',
        title='Role'
    )
    user: Optional[str] = Field(
        default=None,
        description='The user ID of the team member',
        example='1234567890',
        title='User'
    )

    @validator('email', pre=True)
    def validate_email(cls, v):
        return v.lower()

    @validator('role', pre=True)
    def validate_role(cls, v):
        return v.lower()


class TermsAcceptance(Base):
    """Details on the acceptance of the Versify Services Agreement"""
    date: Optional[int] = Field(
        default=None,
        description='The timestamp when the terms were accepted',
        example=1601059200,
        title='Acceptance Timestamp'
    )
    ip: Optional[str] = Field(
        default=None,
        description='The IP address of the user when the terms were accepted',
        example='',
        title='Acceptance IP Address'
    )
    service_agreement: Optional[str] = Field(
        default=None,
        description='The version of the Versify Services Agreement',
        example='1.0',
        title='Acceptance Service Agreement'
    )
    user_agent: Optional[str] = Field(
        default=None,
        description='The user agent of the user when the terms were accepted',
        example='',
        title='Acceptance User Agent'
    )


class Wallet(Base):
    managed: bool = Field(
        default=False,
        description='Whether the wallet is managed by the platform',
        example=False,
        title='Managed'
    )
    private_key: Union[str, None] = Field(
        default=None,
        description='The private key of the wallet',
        example='0x0000000000000000000000000000000000000000000000000000000000000000',
        title='Private Key'
    )
    public_address: str = Field(
        default=None,
        description='The public address of the wallet',
        example='0x0000000000000000000000000000000000000000',
        title='Public Address'
    )
    type: WalletType = Field(
        default=WalletType.ETHEREUM,
        description='The type of the wallet',
        example='ethereum',
        title='Wallet Type'
    )
    verified: bool = Field(
        default=False,
        description='Whether the wallet has been verified by signing a message',
        example=False,
        title='Verified'
    )

    @root_validator(pre=True)
    def default_values(cls, values):
        if values.get('managed', False) and not values.get('private_key', None):
            priv = secrets.token_hex(32)
            private_key = "0x" + priv
            account = EthAccount.privateKeyToAccount(private_key)
            values['managed'] = True
            values['private_key'] = private_key
            values['public_address'] = account.address
            values['type'] = WalletType.ETHEREUM
            values['verified'] = True
        return values


class Offer(Base):
    name: Optional[str] = ''
    description: Optional[str] = ''
    image: Optional[str] = ''
    cta_text: Optional[str] = ''
    cta_url: Optional[str] = ''
    primary_color: Optional[str] = ''
    secondary_color: Optional[str] = ''


class TriggerScheduleConfig(Base):
    at: Optional[int]  # Ex: '1601514370'
    cron: Optional[str]  # Ex: '0 20 * * ? *'
    rate: Optional[str]  # Ex: '5 minutes'
    start: Optional[int]  # Ex: 1601514370
    end: Optional[int]  # Ex: 1601514370


class TriggerConfig(Base):
    schedule: Optional[TriggerScheduleConfig]
    source: str
    detail_type: str
    detail_filters: list[Filter] = []


class Trigger(Base):
    type: TriggerType
    config: TriggerConfig


class ActionConfig(Base):

    # CREATE_NOTE
    note: Optional[str]

    # SEND_APP_MESSAGE / SEND_EMAIL_MESSAGE
    body: Optional[str]
    member: Optional[str]
    subject: Optional[str]
    type: Optional[str]

    # SEND_REWARD
    asset: Optional[str]
    quantity: Optional[int]

    # TAG_CONTACT
    tags: Optional[list[str]]

    # MATCH_ALL/MATCH_ANY
    filters: list[Filter] = []

    # WAIT
    seconds: Optional[int]


class Action(Base):
    type: ActionType = ActionType.WAIT
    comment: Optional[str]
    config: ActionConfig
    end: Optional[bool]
    next: Optional[str]


class RunStateResult(Base):
    name: str = Field(
        ...,
        description='The name of the state',
        example='state_1',
        title='State Name'
    )
    result: dict = Field(
        default={},
        description='The result of the state',
        example={'key': 'value'},
        title='State Result'
    )
    status: RunStatus = Field(
        ...,
        description='The status of the state',
        example=RunStatus.RUNNING,
        title='State Status'
    )
    time_started: int = Field(
        ...,
        description='The timestamp when the state started',
        title='State Started Timestamp'
    )
    time_ended: Optional[int] = Field(
        default=None,
        description='The timestamp when the state ended',
        title='State Ended Timestamp'
    )
