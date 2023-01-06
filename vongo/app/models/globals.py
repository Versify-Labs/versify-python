from typing import Dict, List, Union

from app.models.base import Base, BaseCreate, BaseUpdate
from app.models.enums import (
    ActionType,
    ContactQueryField,
    Operator,
    RunStatus,
    SubscriptionPlan,
    SubscriptionStatus,
    TeamMemberRole,
    TriggerType,
    WalletPosition,
)
from app.models.factory import (
    api_public_key,
    api_secret_key,
    generate_stripe_customer_id,
)
from pydantic import AnyHttpUrl, EmailStr, Field, validator


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
    value: Union[str, int, float, bool, EmailStr, AnyHttpUrl, List[Dict]] = Field(
        ...,
        description="The value to query by",
        example="gmail.com",
        title="Query Value",
    )


class AccountMetrics(Base):

    contacts: int = Field(
        default=0,
        description="The number of contacts in the account",
        example=100,
        title="Contacts",
    )
    journeys: int = Field(
        default=0,
        description="The number of journeys in the account",
        example=100,
        title="Journeys",
    )
    journey_runs: int = Field(
        default=0,
        description="The number of journey runs in the account",
        example=100,
        title="Journey Runs",
    )
    mints: int = Field(
        default=0,
        description="The number of mints in the account",
        example=100,
        title="Mints",
    )
    redemptions: int = Field(
        default=0,
        description="The number of redemptions in the account",
        example=100,
        title="Redemptions",
    )
    rewards: int = Field(
        default=0,
        description="The number of rewards in the account",
        example=100,
        title="Rewards",
    )


class ActionConfig(Base):
    """An action configuration."""

    # CREATE_NOTE
    note: Union[str, None] = Field(
        default=None,
        description="The note to create",
        example="This is a note",
        title="Note",
    )

    # SEND_APP_MESSAGE / SEND_EMAIL_MESSAGE
    body: Union[str, None] = Field(
        default=None,
        description="The body of the message",
        example="This is a message",
        title="Message Body",
    )
    member: Union[str, None] = Field(
        default=None,
        description="The member to send the message to",
        example="member",
        title="Message Member",
    )
    subject: Union[str, None] = Field(
        default=None,
        description="The subject of the message",
        example="This is a message",
        title="Message Subject",
    )
    message_type: Union[str, None] = Field(
        default=None,
        description="The type of the message",
        example="email",
        title="Message Type",
    )

    # SEND_REWARD
    asset: Union[str, None] = Field(
        default=None,
        description="The asset to send",
        example="asset",
        title="Reward Asset",
    )
    quantity: Union[int, None] = Field(
        default=None,
        description="The quantity of the reward",
        example=1,
        title="Reward Quantity",
    )

    # TAG_CONTACT
    tags: Union[list[str], None] = Field(
        default=None,
        description="The tags to add to the contact",
        example=["Customer"],
        title="Tags",
    )

    # MATCH_ALL/MATCH_ANY
    filters: list[Query] = Field(
        default=[],
        description="The filters to match",
        example=[
            {"field": "email", "operator": "EQUALS", "value": ""},
            {"field": "email", "operator": "EQUALS", "value": ""},
        ],
        title="Match Querys",
    )

    # WAIT
    seconds: Union[int, None] = Field(
        default=None,
        description="The number of seconds to wait",
        example=1,
        title="Wait Seconds",
    )


class Action(Base):
    """An action for a journey."""

    action_type: ActionType = Field(
        ...,
        description="The type of action",
        example=ActionType.CREATE_NOTE,
        title="Action Type",
    )
    comment: Union[str, None] = Field(
        default=None,
        description="A comment for the action",
        example="",
        title="Action Comment",
    )
    config: ActionConfig = Field(
        ...,
        description="The configuration for the action",
        title="Action Configuration",
    )
    end: Union[bool, None] = Field(
        default=None,
        description="Whether the action ends the journey",
        example=False,
        title="Action Ends Journey",
    )
    next: Union[str, None] = Field(
        default=None,
        description="The next action to run",
        example="",
        title="Next Action",
    )


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

    logo: Union[AnyHttpUrl, None] = Field(
        default=None,
        description="The URL of the brand's logo",
        example="https://example.com/logo.png",
        title="Logo URL",
    )
    action_color: Union[str, None] = Field(
        default="#000000",
        description="The action color of the brand",
        example="#000000",
        title="Action Color",
    )
    background_color: Union[str, None] = Field(
        default="#000000",
        description="The background color of the brand",
        example="#000000",
        title="Background Color",
    )
    primary_color: Union[str, None] = Field(
        default="#000000",
        description="The primary color of the brand",
        example="#000000",
        title="Primary Color",
    )
    secondary_color: Union[str, None] = Field(
        default="#000000",
        description="The secondary color of the brand",
        example="#000000",
        title="Secondary Color",
    )
    tertiary_color: Union[str, None] = Field(
        default="#000000",
        description="The tertiary color of the brand",
        example="#000000",
        title="Tertiary Color",
    )
    wallet_action_color: Union[str, None] = Field(
        default="#000000",
        description="The wallet action color of the brand",
        example="#000000",
        title="Wallet Action Color",
    )
    wallet_background_color: Union[str, None] = Field(
        default="#000000",
        description="The wallet background color of the brand",
        example="#000000",
        title="Wallet Background Color",
    )
    wallet_display_filters: List[Query] = Field(
        default=[],
        description="The wallet display filters of the brand",
        example=[
            Query(
                field="url",
                operator=Operator.CONTAINS,
                value="example.com/rewards",
            )
        ],
        title="Wallet Display Filters",
    )
    wallet_position: WalletPosition = Field(
        default=WalletPosition.BOTTOM_LEFT,
        description="The wallet position of the brand",
        example=WalletPosition.BOTTOM_LEFT,
        title="Wallet Position",
    )
    wallet_welcome_message: Union[str, None] = Field(
        default="Welcome",
        description="The wallet welcome message of the brand",
        example="Welcome to Acme",
        title="Wallet Welcome Message",
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


class Offer(Base):
    """An offer for a journey."""

    name: Union[str, None] = Field(
        default=None,
        description="The name of the offer",
        example="Free Trial",
        title="Offer Name",
    )
    description: Union[str, None] = Field(
        default=None,
        description="The description of the offer",
        example="A free trial of the product",
        title="Offer Description",
    )
    image: Union[str, None] = Field(
        default=None,
        description="The image of the offer",
        example="https://example.com/image.png",
        title="Offer Image",
    )
    cta_text: Union[str, None] = Field(
        default=None,
        description="The text of the call to action button",
        example="Get Started",
        title="Offer Call to Action Text",
    )
    cta_url: Union[str, None] = Field(
        default=None,
        description="The URL of the call to action button",
        example="https://example.com/get-started",
        title="Offer Call to Action URL",
    )
    primary_color: Union[str, None] = Field(
        default=None,
        description="The primary color of the offer",
        example="#000000",
        title="Offer Primary Color",
    )
    secondary_color: Union[str, None] = Field(
        default=None,
        description="The secondary color of the offer",
        example="#ffffff",
        title="Offer Secondary Color",
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
    time_ended: Union[int, None] = Field(
        default=None,
        description="The timestamp when the state ended",
        title="State Ended Timestamp",
    )


class SocialProfile(Base):
    """A social profile for a contact."""

    name: str = Field(
        ...,
        description="The name of the social network",
        example="Facebook",
        title="Social Network Name",
    )
    url: AnyHttpUrl = Field(
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
    user: Union[str, None] = Field(
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

    date: Union[int, None] = Field(
        default=None,
        description="The timestamp when the terms were accepted",
        example=1601059200,
        title="Acceptance Timestamp",
    )
    ip: Union[str, None] = Field(
        default=None,
        description="The IP address of the user when the terms were accepted",
        example="",
        title="Acceptance IP Address",
    )
    service_agreement: Union[str, None] = Field(
        default=None,
        description="The version of the Versify Services Agreement",
        example="1.0",
        title="Acceptance Service Agreement",
    )
    user_agent: Union[str, None] = Field(
        default=None,
        description="The user agent of the user when the terms were accepted",
        example="",
        title="Acceptance User Agent",
    )


class TriggerScheduleConfig(Base):
    """A trigger schedule configuration."""

    at: Union[int, None] = Field(
        default=None,
        description="The timestamp to trigger the event at",
        example=1601514370,
        title="Trigger Timestamp",
    )
    cron: Union[str, None] = Field(
        default=None,
        description="The cron expression to trigger the event at",
        example="0 20 * * ? *",
        title="Trigger Cron Expression",
    )
    rate: Union[str, None] = Field(
        default=None,
        description="The rate to trigger the event at",
        example="5 minutes",
        title="Trigger Rate",
    )
    start: Union[int, None] = Field(
        default=None,
        description="The timestamp to start triggering the event at",
        example=1601514370,
        title="Trigger Start Timestamp",
    )
    end: Union[int, None] = Field(
        default=None,
        description="The timestamp to stop triggering the event at",
        example=1601514370,
        title="Trigger End Timestamp",
    )


class TriggerConfig(Base):
    """A trigger configuration."""

    schedule: Union[TriggerScheduleConfig, None] = Field(
        default=None,
        description="The schedule configuration for the trigger",
        example={
            "at": 1601514370,
            "cron": "0 20 * * ? *",
            "rate": "5 minutes",
            "start": 1601514370,
            "end": 1601514370,
        },
        title="Trigger Schedule Configuration",
    )
    source: str = Field(
        ...,
        description="The source of the trigger",
        example="contact",
        title="Trigger Source",
    )
    detail_type: str = Field(
        ...,
        description="The detail type of the trigger",
        example="contact.created",
        title="Trigger Detail Type",
    )
    detail_filters: list[Query] = Field(
        default=[],
        description="The detail filters of the trigger",
        example=[
            {"field": "email", "operator": "EQUALS", "value": ""},
            {"field": "email", "operator": "EQUALS", "value": ""},
        ],
        title="Trigger Detail Querys",
    )


class Trigger(Base):
    """A trigger for a journey."""

    trigger_type: TriggerType = Field(
        ...,
        description="The type of trigger",
        example=TriggerType.SCHEDULE,
        title="Trigger Type",
    )
    config: TriggerConfig = Field(
        ...,
        description="The configuration for the trigger",
        example={
            "schedule": {
                "at": 1601514370,
                "cron": "0 20 * * ? *",
                "rate": "5 minutes",
                "start": 1601514370,
                "end": 1601514370,
            },
            "source": "contact",
            "detail_type": "contact.created",
            "detail_filters": [
                {"field": "email", "operator": "EQUALS", "value": ""},
                {"field": "email", "operator": "EQUALS", "value": ""},
            ],
        },
        title="Trigger Configuration",
    )
