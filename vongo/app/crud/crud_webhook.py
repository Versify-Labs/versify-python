from typing import Any, Dict, List, Optional

from app.crud.base import BaseResource
from app.db.session import SessionLocal
from app.models.webhook import Webhook


class WebhookResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Webhooks"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Webhook:
        webhook_body = Webhook(**body)
        self._create(webhook_body.bson())
        return webhook_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Webhook]:
        webhook = self._get(**{"_id": id})
        return Webhook(**webhook) if webhook else None

    def list(self, **kwargs) -> List[Webhook]:
        webhooks = self._list(**kwargs)
        return [Webhook(**webhook) for webhook in webhooks]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Webhook]:
        webhooks = self._search(query=query, **kwargs)
        return [Webhook(**webhook) for webhook in webhooks]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Webhook]:
        webhook = self._update(id, body)
        return Webhook(**webhook) if webhook else None
