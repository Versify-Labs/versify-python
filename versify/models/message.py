from enum import Enum

from ._base import BaseAccountModel


class MessageStatus(str, Enum):
    """The status of a message."""
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'


class MessageType(str, Enum):
    APP = "app"
    EMAIL = "email"


class Message(BaseAccountModel):
    object: str = 'message'
    body: str = ""
    contact: str
    member: str
    status: MessageStatus = MessageStatus.PENDING
    subject: str = ""
    type: MessageType = MessageType.EMAIL
