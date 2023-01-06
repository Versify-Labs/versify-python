from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.redemption import Redemption
from .base import BaseResource


class RedemptionResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Redemptions"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Redemption:
        redemption_body = Redemption(**body)
        self._create(redemption_body.bson())
        return redemption_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Redemption]:
        redemption = self._get(**{"_id": id})
        return Redemption(**redemption) if redemption else None

    def list(self, **kwargs) -> List[Redemption]:
        redemptions = self._list(**kwargs)
        return [Redemption(**redemption) for redemption in redemptions]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Redemption]:
        redemptions = self._search(query=query, **kwargs)
        return [Redemption(**redemption) for redemption in redemptions]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Redemption]:
        redemption = self._update(id, body)
        return Redemption(**redemption) if redemption else None
