from typing import Optional

from .base import Base
from .enums import MessageStatus, MessageType


class Message(Base):
    object: str = "message"
    type: MessageType = MessageType.EMAIL
    content_body: str = ""
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
