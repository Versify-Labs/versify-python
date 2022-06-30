from typing import Optional

from pydantic import Field

from .base import BaseVersifyModel


class Notification(BaseVersifyModel):
    id: Optional[str] = Field(None, alias="_id")
    object: str = 'notification'
    created: int
    metadata: Optional[dict] = {}
    organization: str
    status: str = 'pending'
