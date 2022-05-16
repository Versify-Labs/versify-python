import os
import time

from pynamodb.attributes import (BooleanAttribute, ListAttribute, MapAttribute,
                                 NumberAttribute, UnicodeAttribute,
                                 VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel


class SignatureByObjectByStatus(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByObjectByStatus'
        projection = AllProjection()

    object = UnicodeAttribute(hash_key=True)
    status = UnicodeAttribute(range_key=True)


class SignatureModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='signature')
    status = UnicodeAttribute(null=False, default='pending')
    transaction = UnicodeAttribute(null=True)
    version = VersionAttribute()
    by_object_by_status = SignatureByObjectByStatus()


class TransactionModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    block_hash = UnicodeAttribute(null=True)
    block_num = NumberAttribute(null=True)
    contract_address = UnicodeAttribute(null=True)
    from_address = UnicodeAttribute(null=True)
    id = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='transaction')
    signature = UnicodeAttribute(null=True)
    status = UnicodeAttribute(null=False, default='pending')
    success = BooleanAttribute(null=True)
    timestamp = NumberAttribute(null=False, default=int(time.time()))
    to_address = UnicodeAttribute(null=True)
    type = UnicodeAttribute(null=True)
    version = VersionAttribute()
