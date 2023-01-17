import typing_extensions

from versify.paths import PathValues
from versify.apis.paths.v2_accounts import V2Accounts
from versify.apis.paths.v2_accounts_account_id import V2AccountsAccountId
from versify.apis.paths.v2_accounts_account_id_metrics import V2AccountsAccountIdMetrics
from versify.apis.paths.v2_assets import V2Assets
from versify.apis.paths.v2_assets_search import V2AssetsSearch
from versify.apis.paths.v2_assets_asset_id import V2AssetsAssetId
from versify.apis.paths.v2_auth_authenticate import V2AuthAuthenticate
from versify.apis.paths.v2_auth_login import V2AuthLogin
from versify.apis.paths.v2_auth_register import V2AuthRegister
from versify.apis.paths.v2_claims import V2Claims
from versify.apis.paths.v2_claims_search import V2ClaimsSearch
from versify.apis.paths.v2_claims_claim_id import V2ClaimsClaimId
from versify.apis.paths.v2_collections import V2Collections
from versify.apis.paths.v2_collections_search import V2CollectionsSearch
from versify.apis.paths.v2_collections_collection_id import V2CollectionsCollectionId
from versify.apis.paths.v2_contacts import V2Contacts
from versify.apis.paths.v2_contacts_search import V2ContactsSearch
from versify.apis.paths.v2_contacts_contact_id import V2ContactsContactId
from versify.apis.paths.v2_events import V2Events
from versify.apis.paths.v2_events_search import V2EventsSearch
from versify.apis.paths.v2_events_event_id import V2EventsEventId
from versify.apis.paths.v2_journeys import V2Journeys
from versify.apis.paths.v2_journeys_search import V2JourneysSearch
from versify.apis.paths.v2_journeys_journey_id import V2JourneysJourneyId
from versify.apis.paths.v2_messages import V2Messages
from versify.apis.paths.v2_messages_search import V2MessagesSearch
from versify.apis.paths.v2_messages_message_id import V2MessagesMessageId
from versify.apis.paths.v2_mints import V2Mints
from versify.apis.paths.v2_mints_search import V2MintsSearch
from versify.apis.paths.v2_mints_mint_id import V2MintsMintId
from versify.apis.paths.v2_notes import V2Notes
from versify.apis.paths.v2_notes_search import V2NotesSearch
from versify.apis.paths.v2_notes_note_id import V2NotesNoteId
from versify.apis.paths.v2_oauth_access_token import V2OauthAccessToken
from versify.apis.paths.v2_oauth_authorize import V2OauthAuthorize
from versify.apis.paths.v2_oauth_user_info import V2OauthUserInfo
from versify.apis.paths.v2_redemptions import V2Redemptions
from versify.apis.paths.v2_redemptions_search import V2RedemptionsSearch
from versify.apis.paths.v2_redemptions_redemption_id import V2RedemptionsRedemptionId
from versify.apis.paths.v2_rewards import V2Rewards
from versify.apis.paths.v2_rewards_search import V2RewardsSearch
from versify.apis.paths.v2_rewards_reward_id import V2RewardsRewardId
from versify.apis.paths.v2_tags import V2Tags
from versify.apis.paths.v2_tags_search import V2TagsSearch
from versify.apis.paths.v2_tags_tag_id import V2TagsTagId
from versify.apis.paths.v2_users_me import V2UsersMe
from versify.apis.paths.v2_webhooks import V2Webhooks
from versify.apis.paths.v2_webhooks_search import V2WebhooksSearch
from versify.apis.paths.v2_webhooks_webhook_id import V2WebhooksWebhookId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V2_ACCOUNTS: V2Accounts,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID: V2AccountsAccountId,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID_METRICS: V2AccountsAccountIdMetrics,
        PathValues.V2_ASSETS: V2Assets,
        PathValues.V2_ASSETS_SEARCH: V2AssetsSearch,
        PathValues.V2_ASSETS_ASSET_ID: V2AssetsAssetId,
        PathValues.V2_AUTH_AUTHENTICATE: V2AuthAuthenticate,
        PathValues.V2_AUTH_LOGIN: V2AuthLogin,
        PathValues.V2_AUTH_REGISTER: V2AuthRegister,
        PathValues.V2_CLAIMS: V2Claims,
        PathValues.V2_CLAIMS_SEARCH: V2ClaimsSearch,
        PathValues.V2_CLAIMS_CLAIM_ID: V2ClaimsClaimId,
        PathValues.V2_COLLECTIONS: V2Collections,
        PathValues.V2_COLLECTIONS_SEARCH: V2CollectionsSearch,
        PathValues.V2_COLLECTIONS_COLLECTION_ID: V2CollectionsCollectionId,
        PathValues.V2_CONTACTS: V2Contacts,
        PathValues.V2_CONTACTS_SEARCH: V2ContactsSearch,
        PathValues.V2_CONTACTS_CONTACT_ID: V2ContactsContactId,
        PathValues.V2_EVENTS: V2Events,
        PathValues.V2_EVENTS_SEARCH: V2EventsSearch,
        PathValues.V2_EVENTS_EVENT_ID: V2EventsEventId,
        PathValues.V2_JOURNEYS: V2Journeys,
        PathValues.V2_JOURNEYS_SEARCH: V2JourneysSearch,
        PathValues.V2_JOURNEYS_JOURNEY_ID: V2JourneysJourneyId,
        PathValues.V2_MESSAGES: V2Messages,
        PathValues.V2_MESSAGES_SEARCH: V2MessagesSearch,
        PathValues.V2_MESSAGES_MESSAGE_ID: V2MessagesMessageId,
        PathValues.V2_MINTS: V2Mints,
        PathValues.V2_MINTS_SEARCH: V2MintsSearch,
        PathValues.V2_MINTS_MINT_ID: V2MintsMintId,
        PathValues.V2_NOTES: V2Notes,
        PathValues.V2_NOTES_SEARCH: V2NotesSearch,
        PathValues.V2_NOTES_NOTE_ID: V2NotesNoteId,
        PathValues.V2_OAUTH_ACCESS_TOKEN: V2OauthAccessToken,
        PathValues.V2_OAUTH_AUTHORIZE: V2OauthAuthorize,
        PathValues.V2_OAUTH_USER_INFO: V2OauthUserInfo,
        PathValues.V2_REDEMPTIONS: V2Redemptions,
        PathValues.V2_REDEMPTIONS_SEARCH: V2RedemptionsSearch,
        PathValues.V2_REDEMPTIONS_REDEMPTION_ID: V2RedemptionsRedemptionId,
        PathValues.V2_REWARDS: V2Rewards,
        PathValues.V2_REWARDS_SEARCH: V2RewardsSearch,
        PathValues.V2_REWARDS_REWARD_ID: V2RewardsRewardId,
        PathValues.V2_TAGS: V2Tags,
        PathValues.V2_TAGS_SEARCH: V2TagsSearch,
        PathValues.V2_TAGS_TAG_ID: V2TagsTagId,
        PathValues.V2_USERS_ME: V2UsersMe,
        PathValues.V2_WEBHOOKS: V2Webhooks,
        PathValues.V2_WEBHOOKS_SEARCH: V2WebhooksSearch,
        PathValues.V2_WEBHOOKS_WEBHOOK_ID: V2WebhooksWebhookId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V2_ACCOUNTS: V2Accounts,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID: V2AccountsAccountId,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID_METRICS: V2AccountsAccountIdMetrics,
        PathValues.V2_ASSETS: V2Assets,
        PathValues.V2_ASSETS_SEARCH: V2AssetsSearch,
        PathValues.V2_ASSETS_ASSET_ID: V2AssetsAssetId,
        PathValues.V2_AUTH_AUTHENTICATE: V2AuthAuthenticate,
        PathValues.V2_AUTH_LOGIN: V2AuthLogin,
        PathValues.V2_AUTH_REGISTER: V2AuthRegister,
        PathValues.V2_CLAIMS: V2Claims,
        PathValues.V2_CLAIMS_SEARCH: V2ClaimsSearch,
        PathValues.V2_CLAIMS_CLAIM_ID: V2ClaimsClaimId,
        PathValues.V2_COLLECTIONS: V2Collections,
        PathValues.V2_COLLECTIONS_SEARCH: V2CollectionsSearch,
        PathValues.V2_COLLECTIONS_COLLECTION_ID: V2CollectionsCollectionId,
        PathValues.V2_CONTACTS: V2Contacts,
        PathValues.V2_CONTACTS_SEARCH: V2ContactsSearch,
        PathValues.V2_CONTACTS_CONTACT_ID: V2ContactsContactId,
        PathValues.V2_EVENTS: V2Events,
        PathValues.V2_EVENTS_SEARCH: V2EventsSearch,
        PathValues.V2_EVENTS_EVENT_ID: V2EventsEventId,
        PathValues.V2_JOURNEYS: V2Journeys,
        PathValues.V2_JOURNEYS_SEARCH: V2JourneysSearch,
        PathValues.V2_JOURNEYS_JOURNEY_ID: V2JourneysJourneyId,
        PathValues.V2_MESSAGES: V2Messages,
        PathValues.V2_MESSAGES_SEARCH: V2MessagesSearch,
        PathValues.V2_MESSAGES_MESSAGE_ID: V2MessagesMessageId,
        PathValues.V2_MINTS: V2Mints,
        PathValues.V2_MINTS_SEARCH: V2MintsSearch,
        PathValues.V2_MINTS_MINT_ID: V2MintsMintId,
        PathValues.V2_NOTES: V2Notes,
        PathValues.V2_NOTES_SEARCH: V2NotesSearch,
        PathValues.V2_NOTES_NOTE_ID: V2NotesNoteId,
        PathValues.V2_OAUTH_ACCESS_TOKEN: V2OauthAccessToken,
        PathValues.V2_OAUTH_AUTHORIZE: V2OauthAuthorize,
        PathValues.V2_OAUTH_USER_INFO: V2OauthUserInfo,
        PathValues.V2_REDEMPTIONS: V2Redemptions,
        PathValues.V2_REDEMPTIONS_SEARCH: V2RedemptionsSearch,
        PathValues.V2_REDEMPTIONS_REDEMPTION_ID: V2RedemptionsRedemptionId,
        PathValues.V2_REWARDS: V2Rewards,
        PathValues.V2_REWARDS_SEARCH: V2RewardsSearch,
        PathValues.V2_REWARDS_REWARD_ID: V2RewardsRewardId,
        PathValues.V2_TAGS: V2Tags,
        PathValues.V2_TAGS_SEARCH: V2TagsSearch,
        PathValues.V2_TAGS_TAG_ID: V2TagsTagId,
        PathValues.V2_USERS_ME: V2UsersMe,
        PathValues.V2_WEBHOOKS: V2Webhooks,
        PathValues.V2_WEBHOOKS_SEARCH: V2WebhooksSearch,
        PathValues.V2_WEBHOOKS_WEBHOOK_ID: V2WebhooksWebhookId,
    }
)
