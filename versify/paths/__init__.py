# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from versify.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V2_ACCOUNTS = "/v2/accounts"
    V2_ACCOUNTS_ACCOUNT_ID = "/v2/accounts/{account_id}"
    V2_ACCOUNTS_ACCOUNT_ID_METRICS = "/v2/accounts/{account_id}/metrics"
    V2_ASSETS = "/v2/assets"
    V2_ASSETS_SEARCH = "/v2/assets/search"
    V2_ASSETS_ASSET_ID = "/v2/assets/{asset_id}"
    V2_CLAIMS = "/v2/claims"
    V2_CLAIMS_SEARCH = "/v2/claims/search"
    V2_CLAIMS_CLAIM_ID = "/v2/claims/{claim_id}"
    V2_COLLECTIONS = "/v2/collections"
    V2_COLLECTIONS_SEARCH = "/v2/collections/search"
    V2_COLLECTIONS_COLLECTION_ID = "/v2/collections/{collection_id}"
    V2_CONTACTS = "/v2/contacts"
    V2_CONTACTS_SEARCH = "/v2/contacts/search"
    V2_CONTACTS_CONTACT_ID = "/v2/contacts/{contact_id}"
    V2_EVENTS = "/v2/events"
    V2_EVENTS_SEARCH = "/v2/events/search"
    V2_EVENTS_EVENT_ID = "/v2/events/{event_id}"
    V2_JOURNEYS = "/v2/journeys"
    V2_JOURNEYS_SEARCH = "/v2/journeys/search"
    V2_JOURNEYS_JOURNEY_ID = "/v2/journeys/{journey_id}"
    V2_MESSAGES = "/v2/messages"
    V2_MESSAGES_SEARCH = "/v2/messages/search"
    V2_MESSAGES_MESSAGE_ID = "/v2/messages/{message_id}"
    V2_MINTS = "/v2/mints"
    V2_MINTS_SEARCH = "/v2/mints/search"
    V2_MINTS_MINT_ID = "/v2/mints/{mint_id}"
    V2_NOTES = "/v2/notes"
    V2_NOTES_SEARCH = "/v2/notes/search"
    V2_NOTES_NOTE_ID = "/v2/notes/{note_id}"
    V2_REDEMPTIONS = "/v2/redemptions"
    V2_REDEMPTIONS_SEARCH = "/v2/redemptions/search"
    V2_REDEMPTIONS_REDEMPTION_ID = "/v2/redemptions/{redemption_id}"
    V2_REWARDS = "/v2/rewards"
    V2_REWARDS_SEARCH = "/v2/rewards/search"
    V2_REWARDS_REWARD_ID = "/v2/rewards/{reward_id}"
    V2_TAGS = "/v2/tags"
    V2_TAGS_SEARCH = "/v2/tags/search"
    V2_TAGS_TAG_ID = "/v2/tags/{tag_id}"
    V2_USERS_ME = "/v2/users/me"
    V2_WEBHOOKS = "/v2/webhooks"
    V2_WEBHOOKS_SEARCH = "/v2/webhooks/search"
    V2_WEBHOOKS_WEBHOOK_ID = "/v2/webhooks/{webhook_id}"
