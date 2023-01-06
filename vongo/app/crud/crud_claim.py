from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.claim import Claim
from .base import BaseResource


class ClaimResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Claims"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Claim:
        claim_body = Claim(**body)
        self._create(claim_body.bson())
        return claim_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Claim]:
        claim = self._get(**{"_id": id})
        return Claim(**claim) if claim else None

    def list(self, **kwargs) -> List[Claim]:
        claims = self._list(**kwargs)
        return [Claim(**claim) for claim in claims]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Claim]:
        claims = self._search(query=query, **kwargs)
        return [Claim(**claim) for claim in claims]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Claim]:
        claim = self._update(id, body)
        return Claim(**claim) if claim else None
