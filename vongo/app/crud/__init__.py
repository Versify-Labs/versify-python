from ..db.session import SessionLocal
from .crud_account import AccountResource
from .crud_asset import AssetResource
from .crud_claim import ClaimResource
from .crud_collection import CollectionResource
from .crud_contact import ContactResource
from .crud_event import EventResource
from .crud_journey import JourneyResource, RunResource
from .crud_message import MessageResource
from .crud_mint import MintResource
from .crud_note import NoteResource
from .crud_redemption import RedemptionResource
from .crud_reward import RewardResource
from .crud_tag import TagResource
from .crud_user import UserResource
from .crud_webhook import WebhookResource


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
        self.notes = NoteResource(session)
        self.redemptions = RedemptionResource(session)
        self.runs = RunResource(session)
        self.rewards = RewardResource(session)
        self.tags = TagResource(session)
        self.users = UserResource(session)
        self.webhooks = WebhookResource(session)


versify = Versify()
