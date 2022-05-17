import os
import time

from pynamodb.attributes import (MapAttribute, NumberAttribute,
                                 UnicodeAttribute, VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel


class Wallet(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    avatar = UnicodeAttribute(null=True)
    bio = UnicodeAttribute(null=False, default='')
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    email = UnicodeAttribute(null=False)
    handle = UnicodeAttribute(null=False)
    last_login = NumberAttribute(null=True, default=int(time.time()))
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False)
    object = UnicodeAttribute(null=False, default='wallet')
    phone = UnicodeAttribute(null=True)
    version = VersionAttribute()


class BlockchainAddressByEmailByObjectIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByEmailByObject'
        projection = AllProjection()

    email = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class BlockchainAddress(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    address = UnicodeAttribute(null=False)
    chain = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    description = UnicodeAttribute(null=False, default='')
    email = UnicodeAttribute(null=False)
    id = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='blockchain_address')
    version = VersionAttribute()
    by_email_by_object = BlockchainAddressByEmailByObjectIndex()
