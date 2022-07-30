from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Note(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: Optional[str]
    object: str = 'note'
    attachment: Optional[str]
    created: int
    content: str = ''
    metadata: Optional[dict] = {}
    resource_id: str
    resource_type: str
    updated: Optional[int]
    user: dict
