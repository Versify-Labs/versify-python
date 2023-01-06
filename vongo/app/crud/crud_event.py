from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.event import Event
from .base import BaseResource


class EventResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        self.model = Event
        self.db_name = self.model.__db__
        self.db_collection = self.model.__collection__
        self.collection = db_session.get_collection(self.db_name, self.db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Event:
        event_body = Event(**body)
        self._create(event_body.bson())
        return event_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Event]:
        event = self._get(**{"_id": id})
        return Event(**event) if event else None

    def list(self, **kwargs) -> List[Event]:
        events = self._list(**kwargs)
        return [Event(**event) for event in events]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Event]:
        events = self._search(query=query, **kwargs)
        return [Event(**event) for event in events]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Event]:
        event = self._update(id, body)
        return Event(**event) if event else None
