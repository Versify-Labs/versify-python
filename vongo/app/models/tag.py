from app.models.base import BaseCreate, BaseDoc, BaseUpdate
from app.models.factory import tag_id
from pydantic import Field


class Tag(BaseDoc):
    """A tag document in the database."""

    __db__ = "Dev"
    __collection__ = "Tags"

    id: str = Field(
        alias="_id",
        default_factory=tag_id,
        description="Unique identifier for the tag",
        example="tag_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Tag ID",
    )
    object: str = Field(
        default="tag",
        description='The object type. Always "tag"',
        example="tag",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the tag belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )


class TagCreate(BaseCreate):
    """A tag create request body."""

    pass


class TagUpdate(BaseUpdate):
    """A tag update request body."""

    pass
