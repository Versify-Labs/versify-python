from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.contact import Contact
from .base import BaseResource


class ContactResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        self.model = Contact
        self.db_name = self.model.__db__
        self.db_collection = self.model.__collection__
        self.collection = db_session.get_collection(self.db_name, self.db_collection)

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
