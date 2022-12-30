import secrets
import time

from app.core.constants import DEFAULT_LOGO
from bson.objectid import ObjectId
from eth_account import Account as EthAccount

from .enums import ObjectPrefixes


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def object_id(prefix: str) -> str:
    """Generates a new object ID

    Args:
        prefix (str): The object ID prefix

    Returns:
        str: The new object ID
    """
    return f'{prefix}_{PyObjectId()}'


def account_id() -> str:
    """Generates a new account ID

    Returns:
        str: The new account ID
    """
    return object_id(ObjectPrefixes.ACCOUNT)


def asset_id() -> str:
    """Generates a new asset ID

    Returns:
        str: The new asset ID
    """
    return object_id(ObjectPrefixes.ASSET)


def claim_id() -> str:
    """Generates a new claim ID

    Returns:
        str: The new claim ID
    """
    return object_id(ObjectPrefixes.CLAIM)


def collection_id() -> str:
    """Generates a new collection ID

    Returns:
        str: The new collection ID
    """
    return object_id(ObjectPrefixes.COLLECTION)


def contact_id() -> str:
    """Generates a new contact ID

    Returns:
        str: The new contact ID
    """
    return object_id(ObjectPrefixes.CONTACT)


def event_id() -> str:
    """Generates a new event ID

    Returns:
        str: The new event ID
    """
    return object_id(ObjectPrefixes.EVENT)


def journey_id() -> str:
    """Generates a new journey ID

    Returns:
        str: The new journey ID
    """
    return object_id(ObjectPrefixes.JOURNEY)


def journey_run_id() -> str:
    """Generates a new journey run ID

    Returns:
        str: The new journey run ID
    """
    return object_id(ObjectPrefixes.JOURNEY_RUN)


def message_id() -> str:
    """Generates a new message ID

    Returns:
        str: The new message ID
    """
    return object_id(ObjectPrefixes.MESSAGE)


def mint_id() -> str:
    """Generates a new mint ID

    Returns:
        str: The new mint ID
    """
    return object_id(ObjectPrefixes.MINT)


def redemption_id() -> str:
    """Generates a new redemption ID

    Returns:
        str: The new redemption ID
    """
    return object_id(ObjectPrefixes.REDEMPTION)


def reward_id() -> str:
    """Generates a new reward ID

    Returns:
        str: The new reward ID
    """
    return object_id(ObjectPrefixes.REWARD)


def user_id() -> str:
    """Generates a new user ID

    Returns:
        str: The new user ID
    """
    return object_id(ObjectPrefixes.USER)


def webhook_id() -> str:
    """Generates a new webhook ID

    Returns:
        str: The new webhook ID
    """
    return object_id(ObjectPrefixes.WEBHOOK)


def webhook_event_id() -> str:
    """Generates a new webhook event ID

    Returns:
        str: The new webhook event ID
    """
    return object_id(ObjectPrefixes.WEBHOOK_EVENT)


def current_timestamp() -> int:
    """Returns the current timestamp in seconds

    Returns:
        int: The current timestamp in seconds
    """
    return int(time.time())


def api_public_key() -> str:
    """Generates a new API public key

    Returns:
        str: The new API public key
    """

    return "pk_" + secrets.token_hex(32)


def api_secret_key() -> str:
    """Generates a new API secret key

    Returns:
        str: The new API secret key
    """
    return "sk_" + secrets.token_hex(32)


def generate_avatar(name):
    if name:
        return f"https://avatars.dicebear.com/api/initials/{name[0]}.svg"
    else:
        return DEFAULT_LOGO


def generate_stripe_customer_id():
    # TODO: Implement this properly with Stripe
    return f'cus_{secrets.token_hex(16)}'


def generate_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    account = EthAccount.privateKeyToAccount(private_key)
    public_address = account.address
    return {
        'managed': True,
        'public_address': public_address,
        'private_key': private_key,
        'type': 'ethereum',
        'verified': True,
    }