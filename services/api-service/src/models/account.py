
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .base import BaseVersifyModel

DEFAULT_BUSINESS_TYPE = 'individual'
DEFAULT_COUNTRY = 'US'
DEFAULT_CURRENCY = 'usd'
DEFAULT_LOGO = 'https://uploads-ssl.webflow.com/61f99f3055f0fb37c1005252/61f99f3155f0fb4ba7005411_image-2-help-center-saas-x-template.svg'
DEFAULT_PRIMARY_COLOR = '#4457FF'
DEFAULT_SERVICE_AGREEMENT = 'standard'
DEFAULT_SECONDARY_COLOR = '#FF5F85'
DEFAULT_SUBSCRIPTION_PLAN = 'basic'


class Branding(BaseModel):
    """Branding used to apply the account's emails, invoices, links, etc"""
    icon: Optional[str]
    logo: Optional[str] = DEFAULT_LOGO
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


class BillingDetails(BaseModel):
    """Maps to Stripe object"""
    address: Optional[dict]
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]


class Card(BaseModel):
    """Maps to Stripe object"""
    brand: Optional[str]
    exp_month: Optional[int]
    exp_year: Optional[int]
    last4: Optional[str]


class PaymentMethod(BaseModel):
    """Maps to Stripe object"""
    id: Optional[str]
    object: Optional[str]
    billing_details: Optional[BillingDetails]
    card: Optional[Card]
    type: Optional[str]


class InvoiceSettings(BaseModel):
    """Maps to Stripe object"""
    default_payment_method: Optional[PaymentMethod]


class Plan(BaseModel):
    """Maps to Stripe object"""
    id: Optional[str]
    object: Optional[str]
    active: Optional[str]
    aggregate_usage: Optional[str]
    amount: Optional[int]
    billing_schema: Optional[int]
    interval: Optional[str]
    interval_count: Optional[int]
    nickname: Optional[str]
    product: Optional[str]
    tiers_mode: Optional[str]
    usage_type: Optional[str]


class RecurringDetails(BaseModel):
    """Maps to Stripe object"""
    aggregate_usage: Optional[str]
    interval: Optional[str]
    interval_count: Optional[str]
    trial_period_days: Optional[int]
    usage_type: Optional[str]


class PriceTier(BaseModel):
    """Maps to Stripe object"""
    flat_amount: Optional[int]
    unit_amount: Optional[int]
    up_to: Optional[int]


class Price(BaseModel):
    """Maps to Stripe price object"""
    id: Optional[str]
    object: Optional[str]
    active: Optional[str]
    billing_schema: Optional[int]
    currency: Optional[str]
    product: Optional[str]
    tiers: Optional[List[PriceTier]]
    tiers_mode: Optional[str]
    type: Optional[str]
    unit_amount: Optional[int]


class LineItem(BaseModel):
    """Maps to Stripe object"""
    id: Optional[str]
    object: Optional[str]
    amount: Optional[int]
    amount_excluding_tax: Optional[int]
    currency: Optional[str]
    description: Optional[str]
    plan: Optional[Plan]
    price: Optional[Price]
    quantity: Optional[int]
    subscription: Optional[str]
    subscription_item: Optional[str]
    type: Optional[str]


class InvoieLines(BaseModel):
    """Maps to Stripe object"""
    object: Optional[str]
    data: Optional[List[Dict]]
    total_count: Optional[int]
    url: Optional[str]


class SubscriptionItem(BaseModel):
    """Maps to Stripe object"""
    id: Optional[str]
    object: Optional[str]
    plan: Optional[Plan]
    price: Optional[Price]


class SubscriptionItemList(BaseModel):
    """Maps to Stripe object"""
    object: Optional[str]
    data: Optional[List[SubscriptionItem]]
    total_count: Optional[int]


class Subscription(BaseModel):
    """Maps to Stripe object"""
    id: Optional[str]
    object: Optional[str]
    collection_method: Optional[str]
    current_period_end: Optional[int]
    current_period_start: Optional[int]
    items: Optional[SubscriptionItemList]
    latest_invoice: Optional[str]
    plan: Optional[Plan]
    quantity: Optional[int]
    start_date: Optional[int]
    status: Optional[str]
    trial_end: Optional[int]
    trial_start: Optional[int]


class Customer(BaseModel):
    """Maps to Stripe object"""
    id: Optional[str]
    object: Optional[str]
    email: Optional[str]
    invoice_settings: Optional[InvoiceSettings]
    name: Optional[str]


class SubscriptionMap(BaseModel):
    """Maps to Stripe object"""
    __root__: Optional[Subscription]


class Invoice(BaseModel):
    """Maps to Stripe invoice object"""
    object: Optional[str]
    account_name: Optional[str]
    amount_due: Optional[int]
    amount_paid: Optional[int]
    amount_remaining: Optional[str]
    attempt_count: Optional[str]
    attempted: Optional[bool]
    billing_reason: Optional[str]
    collection_method: Optional[str]
    currency: Optional[str]
    lines: Optional[InvoieLines]
    next_payment_attempt: Optional[str]
    paid: Optional[str]
    period_end: Optional[str]
    period_start: Optional[str]
    subscription: Optional[str]
    subtotal: Optional[int]
    subtotal_including_tax: Optional[str]
    total: Optional[int]
    total_discount_amounts: Optional[list] = []
    total_excluding_tax: Optional[int]
    total_tax_amounts: Optional[list] = []


class BillingSettings(BaseModel):
    """Settings used to configure the account's billing plan"""
    customer: Optional[Customer]
    subscriptions: Optional[Dict[str, Subscription]]
    upcoming_invoice: Optional[Invoice]


class DashboardSettings(BaseModel):
    """Settings used to configure the account within the Versify dashboard"""
    name: Optional[str]
    timezone: Optional[str]


class TeamMember(BaseModel):
    email: Optional[str]
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
    email: str
    metadata: Optional[dict] = {}
    settings: Settings
    tos_acceptance: Optional[TermsAcceptance]
    updated: int
