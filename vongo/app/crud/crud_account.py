from typing import Any, Dict, List, Optional

from app.crud.base import BaseResource
from app.db.session import SessionLocal
from app.models.account import Account
from app.models.globals import AccountMetrics


class AccountResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        self.model = Account
        self.db_name = Account.__db__
        self.db_collection = Account.__collection__
        self.collection = db_session.get_collection(self.db_name, self.db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Account:
        account_body = Account(**body)
        self._create(account_body.bson())
        return account_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Account]:
        account = self._get(**{"_id": id})
        return Account(**account) if account else None

    def get_by_id(self, id: str) -> Optional[Account]:
        account = self._get(**{"_id": id})
        return Account(**account) if account else None

    def list(self, **kwargs) -> List[Account]:
        accounts = self._list(**kwargs)
        return [Account(**account) for account in accounts]

    def list_by_email(self, email: str) -> List[Account]:
        return self.list(**{"team.email": email})

    def search(self, query: Dict[str, Any], **kwargs) -> List[Account]:
        accounts = self._search(query=query, **kwargs)
        return [Account(**account) for account in accounts]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Account]:
        account = self._update(id, body)
        return Account(**account) if account else None

    def get_metrics(self, id: str, object_types: Optional[List[str]]) -> AccountMetrics:
        return AccountMetrics()
