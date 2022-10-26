from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..interfaces.versify_model import BaseVersifyModel

DEFAULT_COUNTRY = 'US'
DEFAULT_CURRENCY = 'usd'
DEFAULT_PRIMARY_COLOR = '#4457FF'
DEFAULT_SERVICE_AGREEMENT = 'standard'
DEFAULT_SECONDARY_COLOR = '#FF5F85'


class Branding(BaseModel):
    """Branding used to apply the account's emails, invoices, links, etc"""
    icon: Optional[str]
    logo: Optional[str]
    primary_color: Optional[str] = DEFAULT_PRIMARY_COLOR
    secondary_color: Optional[str] = DEFAULT_SECONDARY_COLOR


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


class AuthSettings(BaseModel):
    """Settings used to configure how this account can be accessed"""
    api_public_key: Optional[str]
    api_secret_key: Optional[str]
    auth0_organization: Optional[str]


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


class Account(BaseVersifyModel):
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
