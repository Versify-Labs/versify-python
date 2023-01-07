from pydantic import Field

from .base import BaseCreate, BaseDoc, BaseUpdate
from .factory import tag_id


class Transaction(BaseDoc):
    """A tag document in the database."""

    __db__ = "Dev"
    __collection__ = "Transactions"

    id: str = Field(
        alias="_id",
        default_factory=tag_id,
        description="Unique identifier for the tag",
        example="tra_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Transaction ID",
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


class TransactionCreate(BaseCreate):
    """A tag create request body."""

    pass


class TransactionUpdate(BaseUpdate):
    """A tag update request body."""

    pass
