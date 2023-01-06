from typing import Any, Dict, List, Optional

from app.crud.base import BaseResource
from app.db.session import SessionLocal
from app.models.note import Note


class NoteResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Notes"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Note:
        note_body = Note(**body)
        self._create(note_body.bson())
        return note_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Note]:
        note = self._get(**{"_id": id})
        return Note(**note) if note else None

    def list(self, **kwargs) -> List[Note]:
        notes = self._list(**kwargs)
        return [Note(**note) for note in notes]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Note]:
        notes = self._search(query=query, **kwargs)
        return [Note(**note) for note in notes]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Note]:
        note = self._update(id, body)
        return Note(**note) if note else None