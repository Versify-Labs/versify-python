from typing import Optional

from ._base import BaseAccountModel


class Webhook(BaseAccountModel):
    object: str = 'webhook'
    active: bool = True
    description: Optional[str]
    enabled_webhook_events: list = []
    updated: Optional[int]
    url: str
