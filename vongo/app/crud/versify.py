from pprint import pprint
from typing import Any, Dict, List, Optional, Tuple, Union

from app.db.session import SessionLocal
from app.models.account import Account
from app.models.asset import Asset
from app.models.claim import Claim
from app.models.collection import Collection
from app.models.contact import Contact
from app.models.enums import Operator
from app.models.event import Event
from app.models.factory import current_timestamp
from app.models.journey import Journey
from app.models.message import Message
from app.models.reward import Reward
from app.models.redemption import Redemption
from app.models.mint import Mint
from app.models.user import User
from app.models.webhook import Webhook
from pymongo import ASCENDING, ReturnDocument


class BaseResource:
    def __init__(self, db_session: SessionLocal):
        db_name = self.__class__.__module__.split(".")[1]
        db_collection = self.__class__.__name__.lower()
        self.collection = db_session.get_collection(db_name, db_collection)

    def _parse_filters(self, **filters: Dict[str, Any]) -> Dict[str, Any]:
        filters_copy = filters.copy()
        for key, value in filters_copy.items():
            if value is None:
                del filters[key]
            elif isinstance(value, list):
                filters[key] = {"$in": value}
            elif isinstance(value, str):
                filters[key] = {"$regex": value}
        return filters

    def _parse_query(self, query: Dict[str, Any] = {}) -> dict:
        # TODO: Handle custom fields

        print()
        print("Query:")
        pprint(query)

        field = query.get("field")
        operator = query.get("operator")
        value = query.get("value")
        print("field:", field)
        print("operator:", operator)
        print("value:", value)

        # Handle logical operators
        if operator == Operator.AND and isinstance(value, list):
            return {"$and": [self._parse_query(q) for q in value]}
        elif operator == Operator.OR and isinstance(value, list):
            return {"$or": [self._parse_query(q) for q in value]}
        elif operator == Operator.NOT and isinstance(value, dict):
            return {"$not": self._parse_query(value)}

        # Handle all types
        elif operator == Operator.EQUALS:
            return {field: value}
        elif operator == Operator.NOT_EQUALS:
            return {field: {"$ne": value}}
        elif operator == Operator.EXISTS:
            return {field: {"$exists": True}}
        elif operator == Operator.NOT_EXISTS:
            return {field: {"$exists": False}}

        # Handle strings
        elif operator == Operator.CONTAINS:
            return {field: {"$regex": value}}
        elif operator == Operator.NOT_CONTAINS:
            return {field: {"$not": {"$regex": value}}}
        elif operator == Operator.STARTS_WITH:
            return {field: {"$regex": f"^{value}"}}
        elif operator == Operator.NOT_STARTS_WITH:
            return {field: {"$not": {"$regex": f"^{value}"}}}
        elif operator == Operator.ENDS_WITH:
            return {field: {"$regex": f"{value}$"}}
        elif operator == Operator.NOT_ENDS_WITH:
            return {field: {"$not": {"$regex": f"{value}$"}}}

        # Handle numbers
        elif operator == Operator.GREATER_THAN:
            return {field: {"$gt": value}}
        elif operator == Operator.GREATER_THAN_OR_EQUAL:
            return {field: {"$gte": value}}
        elif operator == Operator.LESS_THAN:
            return {field: {"$lt": value}}
        elif operator == Operator.LESS_THAN_OR_EQUAL:
            return {field: {"$lte": value}}

        # Handle lists
        elif operator == Operator.IN:
            return {field: {"$in": value}}
        elif operator == Operator.NOT_IN:
            return {field: {"$nin": value}}

        # Return empty dict if no match
        else:
            return {}

    def _create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["created"] = current_timestamp()
        data["updated"] = current_timestamp()
        return self.collection.insert_one(data).inserted_id

    def _count(
        self,
        **filters: Dict[str, Any],
    ) -> int:
        filters = self._parse_filters(**filters)
        return self.collection.count_documents(filters)

    def _delete(
        self,
        **filters: Dict[str, Any],
    ) -> bool:
        filters = self._parse_filters(**filters)
        deleted = self.collection.delete_one(filters).deleted_count
        return deleted > 0

    def _get(
        self,
        **filters: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        filters = self._parse_filters(**filters)
        return self.collection.find_one(filters)

    def _list(
        self,
        page_num: Union[int, None] = None,
        page_size: Union[int, None] = None,
        sort: List[Tuple[str, int]] = [("created", ASCENDING)],
        **filters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        list_args = {}
        if page_num is not None and page_size is not None:
            list_args["limit"] = page_size
            list_args["skip"] = (page_num - 1) * page_size
        if sort:
            list_args["sort"] = sort
        filters = self._parse_filters(**filters)
        return list(self.collection.find(filters, **list_args))

    def _search(
        self,
        page_num: Union[int, None] = None,
        page_size: Union[int, None] = None,
        account: Union[str, None] = None,
        query: Dict[str, Any] = {},
    ) -> List[Dict[str, Any]]:
        list_args = {}
        if page_num is not None and page_size is not None:
            list_args["limit"] = page_size
            list_args["skip"] = (page_num - 1) * page_size
        filters = self._parse_query(query)
        if account:
            filters["account"] = account
        print()
        print("Filters:")
        pprint(filters)
        return list(self.collection.find(filters, **list_args))

    def _update(self, id: str, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates = {}
        for key, value in body.items():
            if value is not None:
                updates[key] = value
        if not updates or len(updates.keys()) < 1:
            return self.collection.find_one({"_id": id})
        updates["updated"] = current_timestamp()
        return self.collection.find_one_andupdate(
            filter={"_id": id},
            update={"$set": updates},
            return_document=ReturnDocument.AFTER,
        )


class AccountResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Accounts"
        self.collection = db_session.get_collection(db_name, db_collection)

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


class AssetResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Assets"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Asset:
        asset_body = Asset(**body)
        self._create(asset_body.bson())
        return asset_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Asset]:
        asset = self._get(**{"_id": id})
        return Asset(**asset) if asset else None

    def list(self, **kwargs) -> List[Asset]:
        assets = self._list(**kwargs)
        return [Asset(**asset) for asset in assets]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Asset]:
        assets = self._search(query=query, **kwargs)
        return [Asset(**asset) for asset in assets]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Asset]:
        asset = self._update(id, body)
        return Asset(**asset) if asset else None


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


class CollectionResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Collections"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Collection:
        collection_body = Collection(**body)
        self._create(collection_body.bson())
        return collection_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Collection]:
        collection = self._get(**{"_id": id})
        return Collection(**collection) if collection else None

    def list(self, **kwargs) -> List[Collection]:
        collections = self._list(**kwargs)
        return [Collection(**collection) for collection in collections]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Collection]:
        collections = self._search(query=query, **kwargs)
        return [Collection(**collection) for collection in collections]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Collection]:
        collection = self._update(id, body)
        return Collection(**collection) if collection else None


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


class EventResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Events"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Event:
        event_body = Event(**body)
        self._create(event_body.bson())
        return event_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Event]:
        event = self._get(**{"_id": id})
        return Event(**event) if event else None

    def list(self, **kwargs) -> List[Event]:
        events = self._list(**kwargs)
        return [Event(**event) for event in events]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Event]:
        events = self._search(query=query, **kwargs)
        return [Event(**event) for event in events]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Event]:
        event = self._update(id, body)
        return Event(**event) if event else None


class JourneyResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Journeys"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Journey:
        journey_body = Journey(**body)
        self._create(journey_body.bson())
        return journey_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Journey]:
        journey = self._get(**{"_id": id})
        return Journey(**journey) if journey else None

    def list(self, **kwargs) -> List[Journey]:
        journeys = self._list(**kwargs)
        return [Journey(**journey) for journey in journeys]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Journey]:
        journeys = self._search(query=query, **kwargs)
        return [Journey(**journey) for journey in journeys]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Journey]:
        journey = self._update(id, body)
        return Journey(**journey) if journey else None


class MessageResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Messages"
        self.collection = db_session.get_collection(db_name, db_collection)

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


class RedemptionResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Redemptions"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Redemption:
        redemption_body = Redemption(**body)
        self._create(redemption_body.bson())
        return redemption_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Redemption]:
        redemption = self._get(**{"_id": id})
        return Redemption(**redemption) if redemption else None

    def list(self, **kwargs) -> List[Redemption]:
        redemptions = self._list(**kwargs)
        return [Redemption(**redemption) for redemption in redemptions]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Redemption]:
        redemptions = self._search(query=query, **kwargs)
        return [Redemption(**redemption) for redemption in redemptions]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Redemption]:
        redemption = self._update(id, body)
        return Redemption(**redemption) if redemption else None


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


class WebhookResource(BaseResource):
    def __init__(self, db_session: SessionLocal):
        db_name = "Dev"
        db_collection = "Webhooks"
        self.collection = db_session.get_collection(db_name, db_collection)

    def count(self, **kwargs) -> int:
        return self._count(**kwargs)

    def create(self, body: Dict[str, Any] = {}) -> Webhook:
        webhook_body = Webhook(**body)
        self._create(webhook_body.bson())
        return webhook_body

    def delete(self, id: str) -> bool:
        return self._delete(**{"_id": id})

    def get(self, id: str) -> Optional[Webhook]:
        webhook = self._get(**{"_id": id})
        return Webhook(**webhook) if webhook else None

    def list(self, **kwargs) -> List[Webhook]:
        webhooks = self._list(**kwargs)
        return [Webhook(**webhook) for webhook in webhooks]

    def search(self, query: Dict[str, Any], **kwargs) -> List[Webhook]:
        webhooks = self._search(query=query, **kwargs)
        return [Webhook(**webhook) for webhook in webhooks]

    def update(self, id: str, body: Dict[str, Any]) -> Optional[Webhook]:
        webhook = self._update(id, body)
        return Webhook(**webhook) if webhook else None


class Versify:
    def __init__(self) -> None:
        session = SessionLocal()
        self.accounts = AccountResource(session)
        self.assets = AssetResource(session)
        self.collections = CollectionResource(session)
        self.contacts = ContactResource(session)
        self.events = EventResource(session)
        self.journeys = JourneyResource(session)
        self.messages = MessageResource(session)
        self.mints = MintResource(session)
        self.redemptions = RedemptionResource(session)
        self.rewards = RewardResource(session)
        self.users = UserResource(session)
        self.webhooks = WebhookResource(session)
