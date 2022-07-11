from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Webhook(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'webhook'
    active: bool = True
    created: int
    description: Optional[str]
    enabled_events: list = []
    metadata: Optional[dict] = {}
    organization: Optional[str]
    url: str
