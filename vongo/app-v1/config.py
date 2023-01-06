import json
import logging
import os

from aws_lambda_powertools.utilities import parameters

from .models import (
    Account,
    Airdrop,
    Claim,
    Collection,
    Contact,
    Event,
    Journey,
    JourneyRun,
    Message,
    Mint,
    MintLink,
    Product,
    Redemption,
    Report,
    Reward,
    User,
    Webhook,
    WebhookEvent,
)

ENV = os.environ["ENVIRONMENT"]
SECRET_NAME = parameters.get_secret(os.environ["SECRET_NAME"])
SECRET = json.loads(SECRET_NAME)  # type: ignore


def get_var(name, default=None):
    if name in os.environ:
        return os.environ[name]
    elif name in SECRET:
        return SECRET[name]
    elif default:
        return default
    else:
        logging.warning(f"Could not find {name} in environment or secrets")
        return None


class Config:
    AWS_ACCOUNT_ID = get_var("AWS_ACCOUNT", "424532774130")
    AWS_REGION = get_var("AWS_REGION", "us-east-1")
    STEP_FUNCTION_LAMBDA_ARN = f"arn:aws:lambda:{AWS_REGION}:{AWS_ACCOUNT_ID}:function:AutomationService-JourneyRunTask"
    STEP_FUNCTION_LOG_ARN = get_var("STEP_FUNCTION_LOG_ARN")
    STEP_FUNCTION_ROLE_ARN = get_var("STEP_FUNCTION_ROLE_ARN")
    STEP_FUNCTION_ARN_BASE = (
        f"arn:aws:states:{AWS_REGION}:{AWS_ACCOUNT_ID}:stateMachine:"
    )


class MandrillConfig:
    MANDRILL_API_KEY = get_var("MANDRILL_API_KEY")


class MongoConfig:
    MONGO_DB_URL = get_var("MONGO_DB_URL")


class ParagonConfig:
    PARAGON_SECRET_KEY = get_var("PARAGON_SECRET_KEY")
    PARAGON_SIGNING_KEY = get_var("PARAGON_SIGNING_KEY")


class S3Config:
    METADATA_BUCKET = "cdn-dev.versifylabs.com"
    METADATA_URI_BASE = "https://cdn-dev.versifylabs.com"
    if ENV == "prod":
        METADATA_BUCKET = "cdn.versifylabs.com"
        METADATA_URI_BASE = "https://cdn.versifylabs.com"


class SlackConfig:
    SLACK_CHANNEL = get_var("SLACK_CHANNEL_ID")
    SLACK_TOKEN = get_var("SLACK_API_TOKEN")


class StripeConfig:
    STRIPE_SECRET_KEY = get_var("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY = get_var("STRIPE_PUBLIC_KEY")
    STRIPE_WEBHOOK_SECRET = get_var("STRIPE_WEBHOOK_SECRET")
    STRIPE_GROWTH_PRICE = get_var("STRIPE_GROWTH_PRICE")


class StytchConfig:
    STYTCH_ENV = "live" if ENV == "prod" else "test"
    STYTCH_SECRET = get_var("STYTCH_SECRET")
    STYTCH_PROJECT_ID = get_var("STYTCH_PROJECT_ID")
    STYTCH_PUBLIC_TOKEN = get_var("STYTCH_PUBLIC_TOKEN")


class TatumConfig:
    TATUM_API_KEY = get_var("TATUM_API_KEY")
    TATUM_API_URL = get_var("TATUM_API_URL")
    TATUM_MATIC_WALLET_ADDRESS = get_var("TATUM_MATIC_WALLET_ADDRESS")
    TATUM_MATIC_WALLET_SIG_ID = get_var("TATUM_MATIC_WALLET_SIG_ID")


class AccountConfig:
    collection = "Accounts"
    db = "Accounts"
    expandables = []
    model = Account
    object = "account"
    prefix = "acct"
    search_index = None


class AirdropConfig:
    collection = "Airdrops"
    db = "Campaigns"
    expandables = ["product"]
    model = Airdrop
    object = "airdrop"
    prefix = "air"
    search_index = "AirdropSearchIndex"


class ClaimConfig:
    collection = "Claims"
    db = "Campaigns"
    expandables = ["contact", "product"]
    model = Claim
    object = "claim"
    prefix = "claim"
    search_index = None


class CollectionConfig:
    collection = "Collections"
    db = "Products"
    expandables = []
    model = Collection
    object = "collection"
    prefix = "coll"
    search_index = None


class ContactConfig:
    collection = "Contacts"
    db = "Contacts"
    expandables = []
    model = Contact
    object = "contact"
    prefix = "cont"
    search_index = "ContactsSearchIndex"


class EventConfig:
    collection = "Events"
    db = "Analytics"
    expandables = ["contact", "product"]
    model = Event
    object = "event"
    prefix = "evt"
    search_index = None


class JourneyConfig:
    collection = "Journeys"
    db = "Campaigns"
    expandables = []
    model = Journey
    object = "journey"
    prefix = "jour"
    search_index = None


class JourneyRunConfig:
    collection = "JourneyRuns"
    db = "Campaigns"
    expandables = ["contact", "journey"]
    model = JourneyRun
    object = "journey_run"
    prefix = "jojourney_run"
    search_index = None


class MessageConfig:
    collection = "Messages"
    db = "Messages"
    expandables = []
    model = Message
    object = "message"
    prefix = "mes"
    search_index = None


class MintConfig:
    collection = "Mints"
    db = "Campaigns"
    expandables = ["collection", "contact", "product"]
    model = Mint
    object = "mint"
    prefix = "mint"
    search_index = None


class MintLinkConfig:
    collection = "MintLinks"
    db = "Campaigns"
    expandables = ["product"]
    model = MintLink
    object = "mint_link"
    prefix = "mlink"
    search_index = None

    # Config for mint links
    MINT_URL = "https://dashboard-dev.versifylabs.com/links"
    if ENV == "prod":
        MINT_URL = "https://dashboard.versifylabs.com/links"


class ProductConfig:
    collection = "Products"
    db = "Products"
    expandables = ["collection"]
    model = Product
    object = "product"
    prefix = "prod"
    search_index = "ProductsSearchIndex"


class RedemptionConfig:
    collection = "Redemptions"
    db = "Campaigns"
    expandables = ["contact", "reward"]
    model = Redemption
    object = "redemption"
    prefix = "red"
    search_index = None


class ReportConfig:
    collection = "Reports"
    db = "Analytics"
    expandables = []
    model = Report
    object = "report"
    prefix = "rep"
    search_index = None


class RewardConfig:
    collection = "Rewards"
    db = "Campaigns"
    expandables = []
    model = Reward
    object = "reward"
    prefix = "rew"
    search_index = None


class UserConfig:
    collection = "Users"
    db = "Accounts"
    expandables = []
    model = User
    object = "user"
    prefix = "user"
    search_index = None


class WebhookConfig:
    collection = "Webhooks"
    db = "Webhooks"
    expandables = []
    model = Webhook
    object = "webhook"
    prefix = "wh"
    search_index = None


class WebhookEventConfig:
    collection = "WebhookEvents"
    db = "Webhooks"
    expandables = []
    model = WebhookEvent
    object = "webhook_event"
    prefix = "whevt"
    search_index = None


def get_service_config(service_name):
    config = {
        "account": AccountConfig,
        "airdrop": AirdropConfig,
        "claim": ClaimConfig,
        "collection": CollectionConfig,
        "contact": ContactConfig,
        "event": EventConfig,
        "journey": JourneyConfig,
        "journey_run": JourneyRunConfig,
        "message": MessageConfig,
        "mint": MintConfig,
        "mint_link": MintLinkConfig,
        "product": ProductConfig,
        "redemption": RedemptionConfig,
        "report": ReportConfig,
        "reward": RewardConfig,
        "user": UserConfig,
        "webhook": WebhookConfig,
        "webhook_event": WebhookEventConfig,
    }
    if service_name in config:
        return config[service_name]
    else:
        raise Exception(f"No config found for {service_name}")
