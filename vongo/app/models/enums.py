from enum import Enum


class ActionType(str, Enum):
    CREATE_NOTE = 'create_note'
    SEND_APP_MESSAGE = 'send_app_message'
    SEND_EMAIL_MESSAGE = 'send_email_message'
    SEND_REWARD = 'send_reward'
    TAG_CONTACT = 'tag_contact'
    MATCH_ALL = 'match_all'
    MATCH_ANY = 'match_any'
    WAIT = 'wait'


class AirdropStatus(str, Enum):
    DRAFT = 'draft'
    SENDING = 'sending'
    PENDING = 'pending'
    ACTIVE = 'active'
    PAUSED = 'paused'
    COMPLETE = 'complete'
    CANCELLED = 'cancelled'


class BlockchainType(str, Enum):
    POLYGON = 'polygon'


class BusinessType(str, Enum):
    BUSINESS = 'business'
    INDIVIDUAL = 'individual'


class ClaimStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class CollectionStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    FAILED = "failed"
    DEPLOYED = "deployed"


class FontEnum(str, Enum):
    INHERIT = "inherit"


class MessageStatus(str, Enum):
    DRAFT = 'draft'
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'


class MessageType(str, Enum):
    APP = "app"
    EMAIL = "email"


class MintStatus(str, Enum):
    RESERVED = "reserved"
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class ObjectPrefixes(str, Enum):
    ACCOUNT = 'act'
    ASSET = 'ast'
    CLAIM = 'clm'
    COLLECTION = 'col'
    CONTACT = 'con'
    EVENT = 'evt'
    JOURNEY = 'jny'
    JOURNEY_RUN = 'jnr'
    MESSAGE = 'msg'
    MINT = 'mnt'
    REDEMPTION = 'rdm'
    REWARD = 'rwd'
    USER = 'usr'
    WEBHOOK = 'whk'
    WEBHOOK_EVENT = 'whe'


class Operator(str, Enum):
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'
    EXISTS = 'exists'
    NOT_EXISTS = 'not_exists'
    STARTS_WITH = 'starts_with'
    NOT_STARTS_WITH = 'not_starts_with'
    ENDS_WITH = 'ends_with'
    NOT_ENDS_WITH = 'not_ends_with'
    GREATER_THAN = 'greater_than'
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal'
    LESS_THAN = 'less_than'
    LESS_THAN_OR_EQUAL = 'less_than_or_equal'


class ReportStatus(str, Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class RewardType(str, Enum):
    COUPON = 'coupon'
    DISCOUNT = 'discount'
    GIFT = 'gift'


class RunStatus(str, Enum):
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class ShapeEnum(str, Enum):
    ROUNDED = "rounded"
    SHARP = "sharp"
    PILL = "pill"


class SubscriptionPlan(str, Enum):
    TRIAL = 'trial'
    GROWTH = 'growth'
    ENTERPRISE = 'enterprise'


class SubscriptionStatus(str, Enum):
    ACTIVE = 'active'
    CANCELED = 'canceled'
    PAST_DUE = 'past_due'
    UNPAID = 'unpaid'


class TeamMemberRole(str, Enum):
    ADMIN = 'admin'
    MEMBER = 'member'
    SUPPORT = 'support'


class TriggerType(str, Enum):
    EVENT = 'event'
    SCHEDULE = 'schedule'


class WalletPosition(str, Enum):
    TOP_LEFT = 'top-left'
    TOP_RIGHT = 'top-right'
    BOTTOM_LEFT = 'bottom-left'
    BOTTOM_RIGHT = 'bottom-right'


class WalletType(str, Enum):
    ETHEREUM = "ethereum"
    SOLANA = "solana"
