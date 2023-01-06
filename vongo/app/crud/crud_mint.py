from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.mint import Mint
from .base import BaseResource


class MintResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Mints"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Mint:
        mint_body = Mint(**body)
        self._create(mint_body.bson())
        return mint_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Mint]:
        mint = self._get(**{"_id": id})
        return Mint(**mint) if mint else None

    def list(self, **kwargs) -> List[Mint]:
        mints = self._list(**kwargs)
        return [Mint(**mint) for mint in mints]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Mint]:
        mints = self._search(query=query, **kwargs)
        return [Mint(**mint) for mint in mints]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Mint]:
        mint = self._update(id, body)
        return Mint(**mint) if mint else None
