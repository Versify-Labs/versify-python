from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field


class BaseVersifyModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str
    created: int
    livemode: Optional[bool] = True
    metadata: Optional[dict] = {}
    updated: Optional[int]

    def to_json(self):
        raw = jsonable_encoder(self, exclude_none=False)
        clean = {'id': raw.pop('_id')}
        clean.update(raw)
        return clean

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class BaseAccountModel(BaseVersifyModel):
    account: str
