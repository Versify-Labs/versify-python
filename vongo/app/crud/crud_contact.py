from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.contact import Contact
from .base import BaseResource


class ContactResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Contacts"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Contact:
        contact_body = Contact(**body)
        self._create(contact_body.bson())
        return contact_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Contact]:
        contact = self._get(**{"_id": id})
        return Contact(**contact) if contact else None

    def list(self, **kwargs) -> List[Contact]:
        contacts = self._list(**kwargs)
        return [Contact(**contact) for contact in contacts]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Contact]:
        contacts = self._search(query=query, **kwargs)
        return [Contact(**contact) for contact in contacts]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Contact]:
        contact = self._update(id, body)
        return Contact(**contact) if contact else None
