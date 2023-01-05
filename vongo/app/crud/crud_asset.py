from typing import Any, Dict, List, Optional

from app.crud.base import BaseResource
from app.db.session import SessionLocal
from app.models.asset import Asset


class AssetResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Assets"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Asset:
        asset_body = Asset(**body)
        self._create(asset_body.bson())
        return asset_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Asset]:
        asset = self._get(**{"_id": id})
        return Asset(**asset) if asset else None

    def list(self, **kwargs) -> List[Asset]:
        assets = self._list(**kwargs)
        return [Asset(**asset) for asset in assets]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Asset]:
        assets = self._search(query=query, **kwargs)
        return [Asset(**asset) for asset in assets]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Asset]:
        asset = self._update(id, body)
        return Asset(**asset) if asset else None