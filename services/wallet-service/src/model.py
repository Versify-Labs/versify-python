import time
from pynamodb.attributes import (MapAttribute,
                                 NumberAttribute, UnicodeAttribute,
                                 VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel


class Profile(PlatformModel):
    class Meta:
        table_name = 'WalletServiceTable'

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    object = UnicodeAttribute(null=False, default='profile')
    avatar = UnicodeAttribute(null=True)
    bio = UnicodeAttribute(null=False, default='')
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    email = UnicodeAttribute(null=False)
    handle = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False)
    phone = UnicodeAttribute(null=True)
    version = VersionAttribute()


class AccountByEmailIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'byObject'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class Account(PlatformModel):
    class Meta:
        table_name = 'WalletServiceTable'

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    object = UnicodeAttribute(null=False, default='account')
    object_index = AccountByEmailIndex()
    address = UnicodeAttribute(null=False)
    chain = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    description = UnicodeAttribute(null=False, default='')
    email = UnicodeAttribute(null=False)
    id = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    version = VersionAttribute()
