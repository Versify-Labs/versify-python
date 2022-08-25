from typing import Optional

from pydantic import Field

from ..interfaces.versify_model import BaseVersifyModel


class Event(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    account: Optional[str]
    object: str = 'event'
    created: int
    data: dict
    metadata: Optional[dict] = {}
    pending_webhooks: int = 0
    request: Optional[dict]
    type: str
    updated: Optional[int]
