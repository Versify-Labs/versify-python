from typing import Any, Dict, List, Optional

from ..db.session import SessionLocal
from ..models.user import User
from .base import BaseResource


class UserResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Users"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> User:
        user_body = User(**body)
        self._create(user_body.bson())
        return user_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[User]:
        user = self._get(**{"_id": id})
        return User(**user) if user else None

    def get_by_email(self, email: str) -> Optional[User]:
        user = self._get(**{"email": email})
        return User(**user) if user else None

    def list(self, **kwargs) -> List[User]:
        users = self._list(**kwargs)
        return [User(**user) for user in users]

    def list_by_email(self, email: str) -> List[User]:
        return self.list(**{"email": email})

    def search(self, query: Dict[str, Any], **kwargs) -> List[User]:
        users = self._search(query=query, **kwargs)
        return [User(**user) for user in users]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[User]:
        user = self._update(id, body)
        return User(**user) if user else None
