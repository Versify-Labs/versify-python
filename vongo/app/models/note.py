from app.models.base import BaseCreate, BaseDoc, BaseUpdate
from app.models.factory import note_id
from pydantic import Field


class Note(BaseDoc):
    """A note document in the database."""

    __db__ = "Dev"
    __collection__ = "Notes"

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
    creator: str = Field(
        ...,
        description="The user who created the note",
        example="usr_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Creator ID",
    )
    note: str = Field(
        default="",
        description="The note",
        example="This is a note",
        title="Note",
    )


class NoteCreate(BaseCreate):
    """A note create request body."""

    pass


class NoteUpdate(BaseUpdate):
    """A note update request body."""

    pass
