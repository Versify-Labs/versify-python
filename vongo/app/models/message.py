from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.enums import MessageStatus, MessageType
from app.models.factory import current_timestamp, message_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import EmailStr, Field


class Message(Base):
    """A message document in the database."""

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
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the message was created",
        example=16,
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
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the message",
        example={"key": "value"},
        title="Metadata",
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
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the user was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )


class MessageCreateRequest(Base):
    """A message create request body."""

    content_body: Union[str, None] = Field(
        default=None,
        description="The body of the message",
        example="",
        title="Body",
    )


class MessageCreateResponse(Message):
    """A message create response body."""

    pass


class MessageDeleteRequest:
    """A message delete request body."""

    pass


class MessageDeleteResponse(Base):
    """A message delete response body."""

    id: str = Field(
        description="Unique identifier for the message",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Message ID",
    )
    object: str = Field(
        default="message",
        description="The object type",
        example="message",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the message has been deleted",
        example=True,
        title="Deleted",
    )


class MessageGetRequest:
    """A message get request body."""

    pass


class MessageGetResponse(Message):
    """A message get response body."""

    pass


class MessageListRequest:
    """A message list request body."""

    def __init__(
        self,
        page_num: int = QueryParam(
            default=1,
            description="The page number to return",
            example=1,
            title="Page Number",
        ),
        page_size: int = QueryParam(
            default=20,
            description="The number of messages to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class MessageListResponse(Base):
    """A message list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of messages returned",
        example=1,
        title="Count",
    )
    data: List[Message] = Field(
        default=[],
        description="The list of messages that match the filters and pagination parameters.",
        title="Messages",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more messages to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/messages",
        description="The URL of the list request",
        example="/v1/messages",
        title="URL",
    )


class MessageSearchRequest(Base):
    """A message search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class MessageSearchResponse(Base):
    """A message search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of messages returned",
        example=1,
        title="Count",
    )
    data: List[Message] = Field(
        default=[],
        description="The list of messages that match the filters and pagination parameters.",
        title="Messages",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more messages to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/messages/search",
        description="The URL of the search request",
        example="/v1/messages/search",
        title="URL",
    )


class MessageUpdateRequest(Base):
    """A message update request body."""

    content_body: Union[str, None] = Field(
        default=None,
        description="The body of the message",
        example="",
        title="Body",
    )


class MessageUpdateResponse(Message):
    """A message update response body."""

    pass
