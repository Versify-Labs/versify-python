from typing import Optional

from ._base import BaseAccountModel


class WebhookEvent(BaseAccountModel):
    object: str = 'webhook_event'
    data: dict
    pending_webhooks: int = 0
    request: Optional[dict]
    type: str
