# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from versify.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ACCOUNTS = "Accounts"
    ASSETS = "Assets"
    AUTH = "Auth"
    CLAIMS = "Claims"
    COLLECTIONS = "Collections"
    CONTACTS = "Contacts"
    EVENTS = "Events"
    JOURNEYS = "Journeys"
    MESSAGES = "Messages"
    MINTS = "Mints"
    NOTES = "Notes"
    REDEMPTIONS = "Redemptions"
    REWARDS = "Rewards"
    TAGS = "Tags"
    USERS = "Users"
    WEBHOOKS = "Webhooks"
