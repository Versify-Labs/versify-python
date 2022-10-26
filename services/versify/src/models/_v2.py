from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..interfaces.versify_model import BaseVersifyModel

DEFAULT_COUNTRY = 'US'
DEFAULT_CURRENCY = 'usd'
DEFAULT_PRIMARY_COLOR = '#4457FF'
DEFAULT_SERVICE_AGREEMENT = 'standard'
DEFAULT_SECONDARY_COLOR = '#FF5F85'


class BlockchainWalletType(str, Enum):
    ethereum = "ethereum"
    bitcoin = "bitcoin"
    bsc = "bsc"
    solana = "solana"


class FontEnum(str, Enum):
    inherit = "inherit"


class ShapeEnum(str, Enum):
    rounded = "rounded"
    sharp = "sharp"
    pill = "pill"


class AuthSettings(BaseModel):
    """Settings used to configure how this account can be accessed"""
    api_public_key: Optional[str]
    api_secret_key: Optional[str]

    # Deprecated
    auth0_organization: Optional[str]


class Branding(BaseModel):
    """Branding used to apply the account's emails, invoices, links, etc"""
    icon: Optional[str]
    logo: Optional[str]
    primary_color: Optional[str] = DEFAULT_PRIMARY_COLOR
    secondary_color: Optional[str] = DEFAULT_SECONDARY_COLOR
    background_color: Optional[str] = "E1E4FF"
    button_color: Optional[str] = "#596AFF"
    font: Optional[FontEnum] = "inherit"  # type: ignore
    icon: Optional[str]
    logo: Optional[str]
    name: Optional[str]
    shapes: Optional[ShapeEnum] = "rounded"  # type: ignore


class BusinessDetails(BaseModel):
    """Internal information about the business"""
    type: Optional[str]


class BusinessProfile(BaseModel):
    """Public information about the business."""
    branding: Branding
    mcc: Optional[str]
    name: Optional[str]
    description: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    url: Optional[str]


class BillingSettings(BaseModel):
    """Settings used to configure the account's billing plan"""
    stripe_customer_id: Optional[str]
    stripe_card_brand: Optional[str]
    stripe_card_exp_month: Optional[int]
    stripe_card_exp_year: Optional[int]
    stripe_card_last4: Optional[str]
    stripe_last_charge_amount: Optional[int]
    stripe_last_charge_at: Optional[int]
    stripe_plan: Optional[str]
    stripe_plan_amount: Optional[int]
    stripe_plan_interval: Optional[str]
    stripe_plan_interval_count: Optional[int]
    stripe_subscription_cancel_at: Optional[int]
    stripe_subscription_cancel_at_period_end: Optional[bool]
    stripe_subscription_period_end: Optional[int]
    stripe_subscription_period_start: Optional[int]
    stripe_subscription_status: Optional[str]
    trial_active: Optional[bool] = True
    trial_mints_available: Optional[int] = 25
    trial_mints_reserved: Optional[int] = 0


class DashboardSettings(BaseModel):
    """Settings used to configure the account within the Versify dashboard"""
    name: Optional[str]
    timezone: Optional[str]


class TeamMember(BaseModel):
    """Information about a user that belongs to a Versify account"""
    email: Optional[EmailStr]
    role: Optional[str] = 'member'


class Settings(BaseModel):
    """Options for customizing how the account functions with Versify"""
    auth: AuthSettings
    billing: BillingSettings
    dashboard: Optional[DashboardSettings]
    team: Optional[List[TeamMember]] = []


class TermsAcceptance(BaseModel):
    """Details on the acceptance of the Versify Services Agreement"""
    date: Optional[int]
    ip: Optional[str]
    service_agreement: Optional[str] = DEFAULT_SERVICE_AGREEMENT
    user_agent: Optional[str]


class Wallet(BaseModel):
    """Information about a wallet that belongs to a Versify account/user"""
    address: str
    index: Optional[int]
    managed: Optional[bool] = False
    type: Optional[BlockchainWalletType] = BlockchainWalletType.ethereum


class Account(BaseVersifyModel):
    """An organization that is a customer of Versify"""
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'account'
    account: str
    active: bool = True
    business_details: Optional[BusinessDetails]
    business_profile: Optional[BusinessProfile]
    country: str = DEFAULT_COUNTRY
    created: int
    currency: str = DEFAULT_CURRENCY
    email: EmailStr
    metadata: Optional[dict] = {}
    settings: Settings
    tos_acceptance: Optional[TermsAcceptance]
    updated: int


class Activity(BaseVersifyModel):
    """An activity used to track a members activity with a Versify account"""
    id: Optional[str] = Field(None, alias="_id")
    account: Optional[str]
    object: str = 'activity'
    created: int
    metadata: Optional[dict] = {}
    type: str


class Asset(BaseVersifyModel):
    """A digital asset that is used to verify membership. A asset belongs to a collection."""
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'asset'
    active: bool = True
    chain: Optional[str] = 'polygon'
    collection: str
    contract_address: Optional[str]
    created: int
    creator_avatar: Optional[str]
    creator_name: Optional[str]
    description: Optional[str]
    image: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    properties: list = []
    tags: list = []
    token_id: Optional[str]
    updated: Optional[int]


class Campaign(BaseVersifyModel):
    """A promotional campaign that can be used to incentivize users to interact with your business

    TODO:
    - Add triggers that can be used to trigger a campaign
    - Add actions that can be used to reward users for interacting with your business
    - Add conditions that can be used to limit the scope of a campaign
    - Add limits that can be used to limit the number of times a campaign can be triggered
    """
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'campaign'
    active: bool = True
    created: int
    description: str = ''
    metadata: Optional[dict] = {}
    name: Optional[str]
    tags: list = []
    updated: Optional[int]


class Collection(BaseVersifyModel):
    """A group of assets. This is equivalent to a smart contract"""
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'collection'
    active: bool = True
    # address of deployed contract
    contract_address: Optional[str]
    created: int
    default: Optional[bool] = False
    description: Optional[str] = 'Default collection'
    image: Optional[str] = 'https://cdn.versifylabs.com/branding/Logos/verisify-logo-transparent-bg.png'
    metadata: Optional[dict] = {}
    name: Optional[str] = 'Default collection'
    signature: Optional[str]
    # updates to pending, then failed or deployed once we receive transaction result
    status: str = 'new'
    tags: list = []
    transaction: Optional[str]
    updated: Optional[int]
    # in s3 bucket that has subfolder for each token_id: https:://s3.aws.{bucket_name}}/{contract_uri}/
    uri: Optional[str]


class DataConnection(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'data_connection'
    active: bool = True
    created: int
    connected: int
    disconnected: int
    metadata: Optional[dict] = {}
    updated: Optional[int]


class Event(BaseVersifyModel):
    """Something that happened within the Versify platform"""
    id: Optional[str] = Field(None, alias="_id")
    account: Optional[str]
    object: str = 'event'
    created: int
    data: dict
    metadata: Optional[dict] = {}
    pending_webhooks: int = 0
    request: Optional[dict]
    type: str


class Member(BaseVersifyModel):
    """A customer of a Versify organization. A member can have multiple assets."""
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'member'
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    created: int
    currency: str = 'usd'
    description: str = ''
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []
    updated: Optional[int]
    wallet_address: Optional[str]
    wallets: Optional[list] = []


class Note(BaseVersifyModel):
    """An internal note that can be used to track information about an object in Versify"""
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'note'
    attachment: Optional[str]
    body: Optional[str] = ''
    created: int
    content: str = ''
    metadata: Optional[dict] = {}
    resource_id: str
    resource_type: str
    updated: Optional[int]
    user: dict


class Reward(BaseVersifyModel):
    """A benefit that can be attached to an asset. A reward can be redeemed by a member."""
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'reward'
    created: int
    contract_address: Optional[str]
    token_id: Optional[str]
    token_quantity_required: Optional[int]
    metadata: Optional[dict] = {}
    updated: Optional[int]
    user: dict


class User(BaseVersifyModel):
    """A user that belongs to a Versify organization"""
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'user'
    active: bool = True
    avatar: Optional[str]
    created: int
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_login: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    phone: Optional[str]
    stytch_user: Optional[str]
    updated: int
    wallets: List[Wallet] = []


class Webhook(BaseVersifyModel):
    """A url that can be set up to receive events from Versify"""
    id: Optional[str] = Field(None, alias="_id")
    account: str
    object: str = 'webhook'
    active: bool = True
    created: int
    description: Optional[str]
    enabled_events: list = []
    metadata: Optional[dict] = {}
    updated: Optional[int]
    url: str
