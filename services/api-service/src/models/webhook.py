from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Webhook(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'webhook'
    active: bool = True
    created: int
    metadata: Optional[dict] = {}
    organization: Optional[str]
