import os
import time

from pynamodb.attributes import (BooleanAttribute, ListAttribute, MapAttribute,
                                 NumberAttribute, UnicodeAttribute,
                                 VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel

"""
Query Patterns

createContact(org_id, data)
listContacts(org_id, query)
getContact(org_id, id)

createTag(org_id, data)

addContactTag(org_id, )
deleteContactTag(org_id, tag_id)

listContactsByTag(org_id, tag_id)

createContactNote(org_id, contact_id, data)
listContactNotes(org_id, contact_id)

createContactEvent(org_id, contact_id, data)
listContactEvent(org_id, contact_id, query)

Store Contacts
PK | SK | id | 
org_123:contact | t
"""


class ListContactsByOrganization(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class Contact(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    archived = BooleanAttribute(null=False, default=False)
    avatar = UnicodeAttribute(null=True)
    billing_addresses = ListAttribute(null=False, default=[])
    blockchain_addresses = ListAttribute(null=False, default=[])
    country = UnicodeAttribute(null=False, default='USA')
    currency = UnicodeAttribute(null=False, default='usd')
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    description = UnicodeAttribute(null=False, default='')
    email = UnicodeAttribute(null=False)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=True)
    object = UnicodeAttribute(null=False, default='contact')
    organization = UnicodeAttribute(null=False)
    phone = UnicodeAttribute(null=True)
    shipping_addresses = ListAttribute(null=False, default=[])
    source = UnicodeAttribute(null=False, default='Versify')
    tags = ListAttribute(null=False, default=[])
    total_airdrops = NumberAttribute(null=False, default=0)
    total_orders = NumberAttribute(null=False, default=0)
    total_spent = NumberAttribute(null=False, default=0)
    version = VersionAttribute()
    by_organization = ListContactsByOrganization()


class ListEventsByContact(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class Event(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    contact = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False, default='')
    object = UnicodeAttribute(null=False, default='activity')
    organization = UnicodeAttribute(null=False)
    version = VersionAttribute()
    by_contact = ListEventsByContact()


class ListNotesByContact(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class Note(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    contact = UnicodeAttribute(null=False)
    content = UnicodeAttribute(null=False, default='')
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='note')
    organization = UnicodeAttribute(null=False)
    sender_avatar = UnicodeAttribute(null=True)
    sender_id = UnicodeAttribute(null=True)
    sender_name = UnicodeAttribute(null=True)
    version = VersionAttribute()
    by_contact = ListNotesByContact()


class ListTagsByContact(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class ListTagsByOrganization(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class Tag(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    description = UnicodeAttribute(null=False, default='')
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False, default='')
    object = UnicodeAttribute(null=False, default='tag')
    organization = UnicodeAttribute(null=False)
    version = VersionAttribute()
    by_contact = ListTagsByContact()
    by_organization = ListTagsByOrganization()
