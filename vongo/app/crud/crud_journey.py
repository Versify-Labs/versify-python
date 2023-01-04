from typing import Any, Dict, List, Optional

from app.crud.base import BaseResource
from app.db.session import SessionLocal
from app.models.journey import Journey


class JourneyResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Journeys"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Journey:
        journey_body = Journey(**body)
        self._create(journey_body.bson())
        return journey_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Journey]:
        journey = self._get(**{"_id": id})
        return Journey(**journey) if journey else None

    def list(self, **kwargs) -> List[Journey]:
        journeys = self._list(**kwargs)
        return [Journey(**journey) for journey in journeys]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Journey]:
        journeys = self._search(query=query, **kwargs)
        return [Journey(**journey) for journey in journeys]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Journey]:
        journey = self._update(id, body)
        return Journey(**journey) if journey else None
