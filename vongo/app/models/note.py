from typing import Any, Dict, List, Union

from app.models.base import Base
from app.models.factory import current_timestamp, note_id
from app.models.globals import Query
from fastapi import Query as QueryParam
from pydantic import Field


class Note(Base):
    id: str = Field(
        alias="_id",
        default_factory=note_id,
        description="Unique identifier for the note",
        example="note_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Note ID",
    )
    object: str = Field(
        default="note",
        description='The object type. Always "note"',
        example="note",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the note belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the note was created",
        example=1601059200,
        title="Created Timestamp",
    )
    creator: str = Field(
        ...,
        description="The user who created the note",
        example="usr_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Creator ID",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the note",
        example={"key": "value"},
        title="Metadata",
    )
    note: str = Field(
        default="",
        description="The note",
        example="This is a note",
        title="Note",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the note was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )


class NoteCreateRequest(Base):
    """A note create request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the note",
        example={"key": "value"},
        title="Metadata",
    )


class NoteCreateResponse(Note):
    """A note create response body."""

    pass


class NoteDeleteRequest:
    """A note delete request body."""

    pass


class NoteDeleteResponse(Base):
    """A note delete response body."""

    id: str = Field(
        description="Unique identifier for the note",
        example="acct_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Note ID",
    )
    object: str = Field(
        default="note",
        description="The object type",
        example="note",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the note has been deleted",
        example=True,
        title="Deleted",
    )


class NoteGetRequest:
    """A note get request body."""

    pass


class NoteGetResponse(Note):
    """A note get response body."""

    pass


class NoteListRequest:
    """A note list request body."""

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
            description="The number of notes to return",
            example=20,
            title="Page Size",
        ),
    ):
        self.page_num = page_num
        self.page_size = page_size


class NoteListResponse(Base):
    """A note list response body."""

    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of notes returned",
        example=1,
        title="Count",
    )
    data: List[Note] = Field(
        default=[],
        description="The list of notes that match the filters and pagination parameters.",
        title="Notes",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more notes to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/notes",
        description="The URL of the list request",
        example="/v1/notes",
        title="URL",
    )


class NoteSearchRequest(Base):
    """A note search request body."""

    query: Query = Field(
        ...,
        description="The query to search for",
        title="Query",
    )


class NoteSearchResponse(Base):
    """A note search response body."""

    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of notes returned",
        example=1,
        title="Count",
    )
    data: List[Note] = Field(
        default=[],
        description="The list of notes that match the filters and pagination parameters.",
        title="Notes",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more notes to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/notes/search",
        description="The URL of the search request",
        example="/v1/notes/search",
        title="URL",
    )


class NoteUpdateRequest(Base):
    """A note update request body."""

    metadata: Union[Dict[str, Any], None] = Field(
        default=None,
        description="Arbitrary metadata associated with the note",
        example={"key": "value"},
        title="Metadata",
    )


class NoteUpdateResponse(Note):
    """A note update response body."""

    pass
