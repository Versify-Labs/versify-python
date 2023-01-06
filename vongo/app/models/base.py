from typing import Any, Dict, Union

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Base(BaseModel):
    """Base model for all other models"""

    class Config:
        """Pydantic config"""

        allow_population_by_field_name = False
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str, set: list}

    def bson(self) -> Dict[str, Any]:
        """Converts the model to a BSON document"""
        return self.dict(by_alias=True)


from app.models.factory import current_timestamp, event_id


class BaseDoc(Base):
    """Base model for all other document models"""

    __db__ = None
    __collection__ = None

    id: Union[str, ObjectId] = Field(
        alias="_id",
        default_factory=ObjectId,
        description="Unique identifier for the object",
        example="obj_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Object ID",
    )
    object: str = Field(
        default="object",
        description='The object type. Always "object"',
        example="object",
        title="Object Type",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the event was created",
        example=1601059200,
        title="Created Timestamp",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the object",
        example={"key": "value"},
        title="Metadata",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the event was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )

    class Config:
        """Pydantic config"""

        allow_population_by_field_name = False
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str, set: list}

    def bson(self) -> Dict[str, Any]:
        """Converts the model to a BSON document"""
        return self.dict(by_alias=True)


class BaseCreate(Base):
    """Base model for all other create models"""

    metadata: Union[dict, None] = Field(
        default=None,
        description="Arbitrary metadata associated with the object",
        example={"key": "value"},
        title="Metadata",
    )


class BaseUpdate(Base):
    """Base model for all other update models"""

    metadata: Union[dict, None] = Field(
        default=None,
        description="Arbitrary metadata associated with the object",
        example={"key": "value"},
        title="Metadata",
    )
