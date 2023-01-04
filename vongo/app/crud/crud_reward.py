from typing import Any, Dict, List, Optional

from app.crud.base import BaseResource
from app.db.session import SessionLocal
from app.models.reward import Reward


class RewardResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Rewards"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Reward:
        reward_body = Reward(**body)
        self._create(reward_body.bson())
        return reward_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Reward]:
        reward = self._get(**{"_id": id})
        return Reward(**reward) if reward else None

    def list(self, **kwargs) -> List[Reward]:
        rewards = self._list(**kwargs)
        return [Reward(**reward) for reward in rewards]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Reward]:
        rewards = self._search(query=query, **kwargs)
        return [Reward(**reward) for reward in rewards]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Reward]:
        reward = self._update(id, body)
        return Reward(**reward) if reward else None
