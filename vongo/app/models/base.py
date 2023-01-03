from typing import Any, Dict

from bson.objectid import ObjectId
from pydantic import BaseModel


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
