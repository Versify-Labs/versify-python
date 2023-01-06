from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.collection import Collection
from .base import BaseResource


class CollectionResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Collections"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Collection:
        collection_body = Collection(**body)
        self._create(collection_body.bson())
        return collection_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Collection]:
        collection = self._get(**{"_id": id})
        return Collection(**collection) if collection else None

    def list(self, **kwargs) -> List[Collection]:
        collections = self._list(**kwargs)
        return [Collection(**collection) for collection in collections]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Collection]:
        collections = self._search(query=query, **kwargs)
        return [Collection(**collection) for collection in collections]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Collection]:
        collection = self._update(id, body)
        return Collection(**collection) if collection else None
