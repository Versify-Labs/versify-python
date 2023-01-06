from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.message import Message
from .base import BaseResource


class MessageResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        self.model = Message
        self.db_name = self.model.__db__
        self.db_collection = self.model.__collection__
        self.collection = db_session.get_collection(self.db_name, self.db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Message:
        message_body = Message(**body)
        self._create(message_body.bson())
        return message_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Message]:
        message = self._get(**{"_id": id})
        return Message(**message) if message else None

    def list(self, **kwargs) -> List[Message]:
        messages = self._list(**kwargs)
        return [Message(**message) for message in messages]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Message]:
        messages = self._search(query=query, **kwargs)
        return [Message(**message) for message in messages]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Message]:
        message = self._update(id, body)
        return Message(**message) if message else None
