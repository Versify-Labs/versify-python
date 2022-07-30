from ..models import (Account, Airdrop, Collection, Contact, Event, Mint,
                      MintLink, Note, Product, User, Webhook)


class AccountConfig:
    collection = 'Accounts'
    db = 'Accounts'
    expandables = []
    model = Account
    object = 'account'
    prefix = 'acct'
    search_index = None


class AirdropConfig:
    collection = 'Airdrops'
    db = 'Campaigns'
    expandables = ['product']
    model = Airdrop
    object = 'airdrop'
    prefix = 'air'
    search_index = None


class CollectionConfig:
    collection = 'Collections'
    db = 'Products'
    expandables = []
    model = Collection
    object = 'collection'
    prefix = 'coll'
    search_index = None


class ContactConfig:
    collection = 'Contacts'
    db = 'Contacts'
    expandables = []
    model = Contact
    object = 'contact'
    prefix = 'cont'
    search_index = 'ContactsSearchIndex'


class EventConfig:
    collection = 'Events'
    db = 'Events'
    expandables = []
    model = Event
    object = 'event'
    prefix = 'evt'
    search_index = None


class MintLinkConfig:
    collection = 'MintLinks'
    db = 'Campaigns'
    expandables = ['product']
    model = MintLink
    object = 'mint_link'
    prefix = 'mlink'
    search_index = None


class MintConfig:
    collection = 'Mints'
    db = 'Campaigns'
    expandables = ['collection', 'contact', 'product']
    model = Mint
    object = 'mint'
    prefix = 'mint'
    search_index = None


class NoteConfig:
    collection = 'Notes'
    db = 'Notes'
    expandables = []
    model = Note
    object = 'note'
    prefix = 'note'
    search_index = None


class ProductConfig:
    collection = 'Products'
    db = 'Products'
    expandables = ['collection']
    model = Product
    object = 'product'
    prefix = 'prod'
    search_index = 'ProductsSearchIndex'


class UserConfig:
    collection = 'Users'
    db = 'Accounts'
    expandables = []
    model = User
    object = 'user'
    prefix = 'user'
    search_index = None


class WebhookConfig:
    collection = 'Webhooks'
    db = 'Events'
    expandables = []
    model = Webhook
    object = 'webhook'
    prefix = 'wh'
    search_index = None


config = {
    'account': AccountConfig,
    'airdrop': AirdropConfig,
    'collection': CollectionConfig,
    'contact': ContactConfig,
    'event': EventConfig,
    'mint_link': MintLinkConfig,
    'mint': MintConfig,
    'note': NoteConfig,
    'product': ProductConfig,
    'user': UserConfig,
    'webhook': WebhookConfig
}
