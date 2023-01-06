from typing import List, Union

from app.models.base import BaseCreate, BaseDoc, BaseUpdate
from app.models.enums import MessageStatus, MessageType
from app.models.factory import message_id
from pydantic import EmailStr, Field


class Message(BaseDoc):
    """A message document in the database."""

    __db__ = "Dev"
    __collection__ = "Messages"

    id: str = Field(
        alias="_id",
        default_factory=message_id,
        description="Unique identifier for the message",
        example="clm_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="User ID",
    )
    object: str = Field(
        default="message",
        description='The object type. Always "message"',
        example="message",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the message belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    bcc_list: List[EmailStr] = Field(
        default=[],
        description="The bcc list of the message",
        example=[],
        title="BCC List",
    )
    cc_list: List[EmailStr] = Field(
        default=[],
        description="The cc list of the message",
        example=[],
        title="CC List",
    )
    content_body: str = Field(
        default="",
        description="The body of the message",
        example="",
        title="Body",
    )
    content_subject: Union[str, None] = Field(
        default=None,
        description="The subject of the message",
        example="",
        title="Subject",
    )
    content_preheader: Union[str, None] = Field(
        default=None,
        description="The preheader of the message",
        example="",
        title="Preheader",
    )
    from_email: Union[EmailStr, None] = Field(
        default=None,
        description="The from email of the message",
        example="",
        title="From Email",
    )
    from_name: Union[str, None] = Field(
        default=None,
        description="The from name of the message",
        example="",
        title="From Name",
    )
    message_type: MessageType = Field(
        default=MessageType.EMAIL,
        description="The type of the message",
        example=MessageType.EMAIL,
        title="Type",
    )
    reply_to_email: Union[EmailStr, None] = Field(
        default=None,
        description="The reply to email of the message",
        example="",
        title="Reply To Email",
    )
    status: str = Field(
        default=MessageStatus.DRAFT,
        description="The status of the message",
        example=MessageStatus.DRAFT,
        title="Status",
    )
    to_contact: Union[str, None] = Field(
        default=None,
        description="The to contact of the message",
        example="",
        title="To Contact",
    )
    to_email: Union[EmailStr, None] = Field(
        default=None,
        description="The to email of the message",
        example="",
        title="To Email",
    )
    to_name: Union[str, None] = Field(
        default=None,
        description="The to name of the message",
        example="",
        title="To Name",
    )


class MessageCreate(BaseCreate):
    """A message create request body."""

    content_body: Union[str, None] = Field(
        default=None,
        description="The body of the message",
        example="",
        title="Body",
    )


class MessageUpdate(BaseUpdate):
    """A message update request body."""

    content_body: Union[str, None] = Field(
        default=None,
        description="The body of the message",
        example="",
        title="Body",
    )
