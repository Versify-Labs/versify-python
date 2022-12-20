from enum import Enum
from typing import Optional

from ._base import BaseAccountModel


class MessageStatus(str, Enum):
    """The status of a message."""
    DRAFT = 'draft'
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'


class MessageType(str, Enum):
    APP = "app"
    EMAIL = "email"


class Message(BaseAccountModel):
    object: str = 'message'
    type: MessageType = MessageType.EMAIL
    content_body: str = ''
    content_subject: Optional[str]
    content_preheader: Optional[str]
    from_email: Optional[str]
    from_name: Optional[str]
    to_contact: Optional[str]
    to_email: Optional[str]
    to_name: Optional[str]
    cc_list: Optional[list] = []
    bcc_list: Optional[list] = []
    reply_to_email: Optional[str]
    status: MessageStatus = MessageStatus.DRAFT
