import typing_extensions

from versify.apis.tags import TagValues
from versify.apis.tags.accounts_api import AccountsApi
from versify.apis.tags.assets_api import AssetsApi
from versify.apis.tags.claims_api import ClaimsApi
from versify.apis.tags.collections_api import CollectionsApi
from versify.apis.tags.contacts_api import ContactsApi
from versify.apis.tags.events_api import EventsApi
from versify.apis.tags.journeys_api import JourneysApi
from versify.apis.tags.messages_api import MessagesApi
from versify.apis.tags.mints_api import MintsApi
from versify.apis.tags.notes_api import NotesApi
from versify.apis.tags.redemptions_api import RedemptionsApi
from versify.apis.tags.rewards_api import RewardsApi
from versify.apis.tags.tags_api import TagsApi
from versify.apis.tags.users_api import UsersApi
from versify.apis.tags.webhooks_api import WebhooksApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.ASSETS: AssetsApi,
        TagValues.CLAIMS: ClaimsApi,
        TagValues.COLLECTIONS: CollectionsApi,
        TagValues.CONTACTS: ContactsApi,
        TagValues.EVENTS: EventsApi,
        TagValues.JOURNEYS: JourneysApi,
        TagValues.MESSAGES: MessagesApi,
        TagValues.MINTS: MintsApi,
        TagValues.NOTES: NotesApi,
        TagValues.REDEMPTIONS: RedemptionsApi,
        TagValues.REWARDS: RewardsApi,
        TagValues.TAGS: TagsApi,
        TagValues.USERS: UsersApi,
        TagValues.WEBHOOKS: WebhooksApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.ASSETS: AssetsApi,
        TagValues.CLAIMS: ClaimsApi,
        TagValues.COLLECTIONS: CollectionsApi,
        TagValues.CONTACTS: ContactsApi,
        TagValues.EVENTS: EventsApi,
        TagValues.JOURNEYS: JourneysApi,
        TagValues.MESSAGES: MessagesApi,
        TagValues.MINTS: MintsApi,
        TagValues.NOTES: NotesApi,
        TagValues.REDEMPTIONS: RedemptionsApi,
        TagValues.REWARDS: RewardsApi,
        TagValues.TAGS: TagsApi,
        TagValues.USERS: UsersApi,
        TagValues.WEBHOOKS: WebhooksApi,
    }
)
