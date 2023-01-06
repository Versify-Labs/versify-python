from enum import Enum
from typing import List, Optional, Type

from pydantic import BaseModel, EmailStr

from ..constants import (
    DEFAULT_COUNTRY,
    DEFAULT_CURRENCY,
    DEFAULT_PRIMARY_COLOR,
    DEFAULT_SECONDARY_COLOR,
    DEFAULT_SERVICE_AGREEMENT,
)
from ._base import BaseAccountModel


class BusinessType(str, Enum):
    BUSINESS = "business"
    INDIVIDUAL = "individual"


class SubscriptionPlan(str, Enum):
    GROWTH = "growth"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"


class TeamMemberRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    SUPPORT = "support"


class WalletPosition(str, Enum):
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class Filter(BaseModel):
    """URL pattern used to configure the account's branding"""

    field: str = "url"
    operator: str = "contains"
    value: str = ""


class Authentication(BaseModel):
    """Settings used to configure how this account can be accessed"""

    api_public_key: str
    api_secret_key: str


class Billing(BaseModel):
    """Settings used to configure the account's billing plan"""

    stripe_customer_id: str

    # Subscription plan
    subscription_plan: Optional[SubscriptionPlan]
    subscription_status: Optional[SubscriptionStatus]
    subscription_trial: bool = True

    # Deprecating these fields in favor of the above
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
    trial_active: Optional[bool]
    trial_mints_available: Optional[int]
    trial_mints_reserved: Optional[int]


class Branding(BaseModel):
    """Branding used to apply the account's emails, invoices, links, etc"""

    display_versify: bool = True
    icon: Optional[str] = None
    logo: Optional[str] = None
    primary_color: str = DEFAULT_PRIMARY_COLOR
    secondary_color: str = DEFAULT_SECONDARY_COLOR
    wallet_action_color: str = DEFAULT_PRIMARY_COLOR
    wallet_background_color: str = DEFAULT_SECONDARY_COLOR
    wallet_display_filters: List[Filter] = []
    wallet_position: WalletPosition = WalletPosition.BOTTOM_RIGHT
    wallet_welcome_message: str = "Welcome to your wallet!"
    website_action_color: str = DEFAULT_PRIMARY_COLOR
    website_background_color: str = DEFAULT_SECONDARY_COLOR
    website_title: str = "Rewards Program | Versify"
    website_hero_title: str = "Rewards Program"
    website_hero_subtitle: str = (
        "Earn points for completing actions and redeem them for rewards."
    )
    website_hero_image: Optional[str] = None


class TeamMember(BaseModel):
    email: EmailStr
    role: TeamMemberRole = TeamMemberRole.MEMBER


class TermsAcceptance(BaseModel):
    """Details on the acceptance of the Versify Services Agreement"""

    date: Optional[int]
    ip: Optional[str]
    service_agreement: Optional[str] = DEFAULT_SERVICE_AGREEMENT
    user_agent: Optional[str]


class Account(BaseAccountModel):
    """Account model."""

    object: str = "account"
    active: bool = True
    authentication: Authentication
    billing: Billing
    branding: Branding
    country: str = DEFAULT_COUNTRY
    currency: str = DEFAULT_CURRENCY
    email: EmailStr
    name: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    team: List[TeamMember] = []
    timezone: str = "America/New_York"
    tos_acceptance: Optional[TermsAcceptance]
    type: BusinessType = BusinessType.BUSINESS
    url: Optional[str]


class AccountCreateRequest(BaseModel):
    branding: Branding
    country: str = DEFAULT_COUNTRY
    currency: str = DEFAULT_CURRENCY
    email: EmailStr
    name: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    timezone: str = "America/New_York"
    tos_acceptance: Optional[TermsAcceptance]
    type: BusinessType = BusinessType.BUSINESS
    url: Optional[str]


class AccountUpdateRequest(BaseModel):
    branding: Branding
    country: str = DEFAULT_COUNTRY
    currency: str = DEFAULT_CURRENCY
    email: EmailStr
    name: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    timezone: str = "America/New_York"
    tos_acceptance: Optional[TermsAcceptance]
    type: BusinessType = BusinessType.BUSINESS
    url: Optional[str]


class AccountQuery(BaseModel):
    age: int


class AccountAdminResponse(BaseModel):
    id: str
    object: str = "account"
    active: bool = True
    authentication: Authentication
    billing: Billing
    branding: Branding
    country: str = DEFAULT_COUNTRY
    currency: str = DEFAULT_CURRENCY
    email: EmailStr
    name: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    team: List[TeamMember] = []
    timezone: str = "America/New_York"
    tos_acceptance: Optional[TermsAcceptance]
    type: BusinessType = BusinessType.BUSINESS
    url: Optional[str]


class AccountMemberResponse(BaseModel):
    id: str
    object: str = "account"
    active: bool = True
    branding: Branding
    country: str = DEFAULT_COUNTRY
    currency: str = DEFAULT_CURRENCY
    email: EmailStr
    name: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    team: List[TeamMember] = []
    timezone: str = "America/New_York"
    tos_acceptance: Optional[TermsAcceptance]
    type: BusinessType = BusinessType.BUSINESS
    url: Optional[str]


class AccountPublicResponse(BaseModel):
    id: str
    branding: Branding
    name: Optional[str]
    support_email: Optional[str]
    support_phone: Optional[str]
    support_url: Optional[str]
    url: Optional[str]


class AccountDeletedResponse(BaseModel):
    id: str
    object: str = "account"
    deleted: bool = True


class AccountListResponse(BaseModel):
    object: str = "list"
    url: str = "/v2/accounts"
    has_more: bool = False
    data: list = []
    count: Optional[int]


def get_response_for_role(self, role: TeamMemberRole) -> Type[BaseModel]:
    if role == TeamMemberRole.ADMIN:
        return AccountAdminResponse
    elif role == TeamMemberRole.MEMBER:
        return AccountMemberResponse
    else:
        return AccountPublicResponse
