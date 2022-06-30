from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Note(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'note'
    attachment: Optional[str]
    created: int
    content: str = ''
    metadata: Optional[dict] = {}
    organization: Optional[str]
    resource_id: str
    resource_type: str
    user: dict
