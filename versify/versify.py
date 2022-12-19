from .services.account import AccountService
from .services.airdrop import AirdropService
from .services.claim import ClaimService
from .services.collection import CollectionService
from .services.contact import ContactService
from .services.event import EventService
from .services.journey import JourneyService
from .services.journey_run import JourneyRunService
from .services.message import MessageService
from .services.mint import MintService
from .services.mint_link import MintLinkService
from .services.note import NoteService
from .services.product import ProductService
from .services.redemption import RedemptionService
from .services.report import ReportService
from .services.reward import RewardService
from .services.signature import SignatureService
from .services.user import UserService
from .services.webhook import WebhookService
from .services.webhook_event import WebhookEventService


class Versify():

    __version__ = 'v1'

    def __init__(self) -> None:

        # Initialize services based on dependencies
        account = AccountService()
        user = UserService(account)
        contact = ContactService()
        claim = ClaimService(contact)
        collection = CollectionService()
        event = EventService(contact)
        journey = JourneyService()
        message = MessageService(contact, user)
        note = NoteService()
        product = ProductService(account, collection)
        report = ReportService()
        webhook = WebhookService()
        webhook_event = WebhookEventService()
        mint_link = MintLinkService(account)
        airdrop = AirdropService(account, contact, mint_link, product)
        mint = MintService(airdrop, contact, mint_link, product, user)
        journey_run = JourneyRunService(contact, journey, mint)
        signature = SignatureService(collection, mint)
        reward = RewardService()
        redemption = RedemptionService(contact, reward)

        # Set services for external use
        self.account_service = account
        self.airdrop_service = airdrop
        self.claim_service = claim
        self.collection_service = collection
        self.contact_service = contact
        self.event_service = event
        self.journey_service = journey
        self.journey_run_service = journey_run
        self.message_service = message
        self.mint_service = mint
        self.mint_link_service = mint_link
        self.note_service = note
        self.product_service = product
        self.redemption_service = redemption
        self.report_service = report
        self.reward_service = reward
        self.signature_service = signature
        self.user_service = user
        self.webhook_service = webhook
        self.webhook_event_service = webhook_event

    def get_version(self) -> str:
        """Get the current version of the Versify API"""
        return self.__version__
