from typing import Dict, List, Optional, Union

from app.models.base import Base
from app.models.enums import (
    ActionType,
    ContactQueryField,
    Operator,
    RunStatus,
    SubscriptionPlan,
    SubscriptionStatus,
    TeamMemberRole,
    TriggerType,
)
from app.models.factory import (
    api_public_key,
    api_secret_key,
    generate_stripe_customer_id,
)
from pydantic import EmailStr, Field, HttpUrl, validator


class Authentication(Base):
    """Settings used to configure how this account can be accessed."""

    api_public_key: str = Field(
        default_factory=api_public_key,
        description="The public key used to authenticate with the API",
        example="pk_123",
        title="API Public Key",
    )
    api_secret_key: str = Field(
        default_factory=api_secret_key,
        description="The secret key used to authenticate with the API",
        example="sk_123",
        title="API Secret Key",
    )


class Author(Base):
    """Author of a piece of content."""

    id: str = Field(
        ...,
        description="The ID of the author",
        example="usr_1232313123123123132",
        title="Author ID",
    )
    name: str = Field(
        ...,
        description="The name of the author",
        example="Jane Doe",
        title="Author Name",
    )


class Billing(Base):
    """Billing information for an account."""

    stripe_customer_id: str = Field(
        default_factory=generate_stripe_customer_id,
        description="The Stripe customer ID",
        example="cus_123",
        title="Stripe Customer ID",
    )
    subscription_plan: SubscriptionPlan = Field(
        default=SubscriptionPlan.TRIAL,
        description="The subscription plan",
        example="growth",
        title="Subscription Plan",
    )
    subscription_status: SubscriptionStatus = Field(
        default=SubscriptionStatus.ACTIVE,
        description="The subscription status",
        example="active",
        title="Subscription Status",
    )


class Brand(Base):
    """A brand used to customize the look and feel of an account."""

    logo: Union[HttpUrl, None] = Field(
        default=None,
        description="The URL of the brand's logo",
        example="https://example.com/logo.png",
        title="Logo URL",
    )
    action_color: Union[str, None] = Field(
        default=None,
        description="The action color of the brand",
        example="#000000",
        title="Action Color",
    )
    background_color: Union[str, None] = Field(
        default=None,
        description="The background color of the brand",
        example="#000000",
        title="Background Color",
    )
    primary_color: Union[str, None] = Field(
        default=None,
        description="The primary color of the brand",
        example="#000000",
        title="Primary Color",
    )
    secondary_color: Union[str, None] = Field(
        default=None,
        description="The secondary color of the brand",
        example="#000000",
        title="Secondary Color",
    )
    tertiary_color: Union[str, None] = Field(
        default=None,
        description="The tertiary color of the brand",
        example="#000000",
        title="Tertiary Color",
    )


class Filter(Base):
    """A filter that can be used to filter data."""

    field: str = Field(
        ...,
        description="The field to filter the data on",
        example=ContactQueryField.EMAIL,
        title="Filter Field",
    )
    operator: Operator = Field(
        ...,
        description="The operator to use",
        example=Operator.ENDS_WITH,
        title="Filter Operator",
    )
    value: str = Field(
        ...,
        description="The value to filter by",
        example="gmail.com",
        title="Filter Value",
    )


class IdentityProvider(Base):
    """An identity provider for a user."""

    provider_type: str = Field(
        ...,
        description="The type of the identity provider",
        example="google",
        title="Provider Type",
    )
    provider_subject: str = Field(
        ...,
        description="The subject of the identity provider",
        example="1234567890",
        title="Provider Subject",
    )


class Location(Base):
    """A location for a person."""

    city: str = Field(
        ...,
        description="The city of the location",
        example="San Francisco",
        title="City",
    )
    country: str = Field(
        ...,
        description="The country of the location",
        example="United States",
        title="Country",
    )
    region: str = Field(
        ...,
        description="The region of the location",
        example="CA",
        title="Region",
    )


class Note(Base):
    """A note for a resource."""

    id: str = Field(
        ...,
        description="The ID of the note",
        example="not_12312312312312",
        title="Note ID",
    )
    author: Author = Field(
        ...,
        description="The creator of the note. Contains user ID, name, etc.",
        title="Note Author",
    )
    created: int = Field(
        ...,
        description="The timestamp of when the note was created",
        example=1629023389,
        title="Created Timestamp",
    )
    content: str = Field(
        default="",
        description="The content of the note",
        example="This is a note",
        title="Note Content",
    )


class PersonName(Base):
    """A person's name."""

    first_name: Union[str, None] = Field(
        default=None,
        description="The first name of the person",
        example="Jane",
        title="First Name",
    )
    middle_name: Union[str, None] = Field(
        default=None,
        description="The middle name of the person",
        example="Middle",
        title="Middle Name",
    )
    last_name: Union[str, None] = Field(
        default=None,
        description="The last name of the person",
        example="Doe",
        title="Last Name",
    )

    @validator("first_name", "middle_name", "last_name", pre=True)
    def validate_names(cls, v):
        if not v:
            return None
        if not v.isalpha():
            raise ValueError("Names must only contain letters")
        return v.title()


class Query(Base):
    """A query that can be used to filter data."""

    field: Union[str, None] = Field(
        default=None,
        description="The field to query the data on",
        example=ContactQueryField.EMAIL,
        title="Query Field",
    )
    operator: Operator = Field(
        ...,
        description="The operator to use",
        example=Operator.EQUALS,
        title="Query Operator",
    )
    value: Union[str, int, float, bool, EmailStr, HttpUrl, List[Dict]] = Field(
        ...,
        description="The value to query by",
        example="gmail.com",
        title="Query Value",
    )


class SocialProfile(Base):
    """A social profile for a contact."""

    name: str = Field(
        ...,
        description="The name of the social network",
        example="Facebook",
        title="Social Network Name",
    )
    url: HttpUrl = Field(
        ...,
        description="The URL of the social profile",
        example="https://www.facebook.com/jane.doe",
        title="Social Profile URL",
    )


class TeamMember(Base):
    """A team member."""

    email: EmailStr = Field(
        ...,
        description="The email of the team member",
        example="jane@example.com",
        title="Email",
    )
    role: TeamMemberRole = Field(
        default=TeamMemberRole.MEMBER,
        description="The role of the team member",
        example="member",
        title="Role",
    )
    user: Optional[str] = Field(
        default=None,
        description="The user ID of the team member",
        example="1234567890",
        title="User",
    )

    @validator("email", pre=True)
    def validate_email(cls, v):
        return v.lower()

    @validator("role", pre=True)
    def validate_role(cls, v):
        return v.lower()


class TermsAcceptance(Base):
    """Details on the acceptance of the Versify Services Agreement"""

    date: Optional[int] = Field(
        default=None,
        description="The timestamp when the terms were accepted",
        example=1601059200,
        title="Acceptance Timestamp",
    )
    ip: Optional[str] = Field(
        default=None,
        description="The IP address of the user when the terms were accepted",
        example="",
        title="Acceptance IP Address",
    )
    service_agreement: Optional[str] = Field(
        default=None,
        description="The version of the Versify Services Agreement",
        example="1.0",
        title="Acceptance Service Agreement",
    )
    user_agent: Optional[str] = Field(
        default=None,
        description="The user agent of the user when the terms were accepted",
        example="",
        title="Acceptance User Agent",
    )


class Offer(Base):
    """An offer for a journey."""

    name: Optional[str] = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    cta_text: Optional[str] = ""
    cta_url: Optional[str] = ""
    primary_color: Optional[str] = ""
    secondary_color: Optional[str] = ""


class TriggerScheduleConfig(Base):
    """A trigger schedule configuration."""

    at: Optional[int]  # Ex: '1601514370'
    cron: Optional[str]  # Ex: '0 20 * * ? *'
    rate: Optional[str]  # Ex: '5 minutes'
    start: Optional[int]  # Ex: 1601514370
    end: Optional[int]  # Ex: 1601514370


class TriggerConfig(Base):
    """A trigger configuration."""

    schedule: Optional[TriggerScheduleConfig]
    source: str
    detail_type: str
    detail_filters: list[Filter] = []


class Trigger(Base):
    """A trigger for a journey."""

    type: TriggerType
    config: TriggerConfig


class ActionConfig(Base):
    """An action configuration."""

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
    """An action for a journey."""

    type: ActionType = ActionType.WAIT
    comment: Optional[str]
    config: ActionConfig
    end: Optional[bool]
    next: Optional[str]


class RunStateResult(Base):
    """The result of a run state."""

    name: str = Field(
        ...,
        description="The name of the state in the run",
        example="state_1",
        title="State Name",
    )
    result: dict = Field(
        default={},
        description="The result of the state",
        example={"key": "value"},
        title="State Result",
    )
    status: RunStatus = Field(
        ...,
        description="The status of the state",
        example=RunStatus.RUNNING,
        title="State Status",
    )
    time_started: int = Field(
        ...,
        description="The timestamp when the state started",
        title="State Started Timestamp",
    )
    time_ended: Optional[int] = Field(
        default=None,
        description="The timestamp when the state ended",
        title="State Ended Timestamp",
    )
