import os

from pynamodb.attributes import (MapAttribute, NumberAttribute,
                                 UnicodeAttribute, VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel


class ListAccountsByWallet(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class AccountModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    address = UnicodeAttribute(null=False)
    chain = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    description = UnicodeAttribute(null=False, default='')
    email = UnicodeAttribute(null=False)
    issuer = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='account')
    version = VersionAttribute()
    wallet = UnicodeAttribute(null=False)
    by_wallet = ListAccountsByWallet()
