from enum import Enum


class AccountStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ActionType(str, Enum):
    CREATE_NOTE = "create_note"
    SEND_APP_MESSAGE = "send_app_message"
    SEND_EMAIL_MESSAGE = "send_email_message"
    SEND_REWARD = "send_reward"
    TAG_CONTACT = "tag_contact"
    MATCH_ALL = "match_all"
    MATCH_ANY = "match_any"
    WAIT = "wait"


class AirdropStatus(str, Enum):
    DRAFT = "draft"
    SENDING = "sending"
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"
    CANCELLED = "cancelled"


class AssetStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class BlockchainType(str, Enum):
    POLYGON = "polygon"


class BusinessType(str, Enum):
    BUSINESS = "business"
    INDIVIDUAL = "individual"


class ClaimStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class ContactStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class ContactQueryField(str, Enum):
    CREATED = "created"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    STATUS = "status"
    UPDATED = "updated"


class CollectionStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    FAILED = "failed"
    DEPLOYED = "deployed"


class FontEnum(str, Enum):
    INHERIT = "inherit"


class MessageStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class MessageType(str, Enum):
    APP = "app"
    EMAIL = "email"


class MintStatus(str, Enum):
    RESERVED = "reserved"
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class ObjectPrefixes(str, Enum):
    ACCOUNT = "act"
    ASSET = "ast"
    CLAIM = "clm"
    COLLECTION = "col"
    CONTACT = "con"
    EVENT = "evt"
    JOURNEY = "jny"
    MESSAGE = "msg"
    MINT = "mnt"
    NOTE = "nte"
    REDEMPTION = "rdm"
    REWARD = "rwd"
    RUN = "run"
    TAG = "tag"
    USER = "usr"
    WALLET = "wlt"
    WEBHOOK = "whk"
    WEBHOOK_EVENT = "whe"


class Operator(str, Enum):

    # Logical
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    # All
    EQUALS = "="
    NOT_EQUALS = "!="
    EXISTS = "EXISTS"
    NOT_EXISTS = "!EXISTS"

    # String
    CONTAINS = "~"
    NOT_CONTAINS = "!~"
    STARTS_WITH = "^"
    NOT_STARTS_WITH = "!^"
    ENDS_WITH = "$"
    NOT_ENDS_WITH = "!$"

    # Integer
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="

    # Array
    IN = "IN"
    NOT_IN = "NIN"


class ReportStatus(str, Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class RewardType(str, Enum):
    COUPON = "coupon"
    DISCOUNT = "discount"
    GIFT = "gift"


class RunStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ShapeEnum(str, Enum):
    ROUNDED = "rounded"
    SHARP = "sharp"
    PILL = "pill"


class SubscriptionPlan(str, Enum):
    TRIAL = "trial"
    GROWTH = "growth"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"


class TeamMemberRole(str, Enum):
    ADMIN = "admin"
    GUEST = "guest"
    MEMBER = "member"
    SUPPORT = "support"


class TriggerType(str, Enum):
    EVENT = "event"
    SCHEDULE = "schedule"


class WalletPosition(str, Enum):
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class WalletType(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
