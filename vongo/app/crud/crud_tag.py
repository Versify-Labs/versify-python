from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.tag import Tag
from .base import BaseResource


class TagResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Tags"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Tag:
        tag_body = Tag(**body)
        self._create(tag_body.bson())
        return tag_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Tag]:
        tag = self._get(**{"_id": id})
        return Tag(**tag) if tag else None

    def list(self, **kwargs) -> List[Tag]:
        tags = self._list(**kwargs)
        return [Tag(**tag) for tag in tags]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Tag]:
        tags = self._search(query=query, **kwargs)
        return [Tag(**tag) for tag in tags]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Tag]:
        tag = self._update(id, body)
        return Tag(**tag) if tag else None
