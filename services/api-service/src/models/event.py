from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Event(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'event'
    created: int
    data: dict
    pending_webhooks: int = 0
    request: Optional[dict]
    type: str
