from app.crud.crud_account import AccountResource
from app.crud.crud_asset import AssetResource
from app.crud.crud_claim import ClaimResource
from app.crud.crud_collection import CollectionResource
from app.crud.crud_contact import ContactResource
from app.crud.crud_event import EventResource
from app.crud.crud_journey import JourneyResource
from app.crud.crud_message import MessageResource
from app.crud.crud_mint import MintResource
from app.crud.crud_redemption import RedemptionResource
from app.crud.crud_reward import RewardResource
from app.crud.crud_user import UserResource
from app.crud.crud_webhook import WebhookResource
from app.db.session import SessionLocal


class Versify:
    def __init__(self) -> None:
        session = SessionLocal()
        self.accounts = AccountResource(session)
        self.assets = AssetResource(session)
        self.claims = ClaimResource(session)
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


versify = Versify()
