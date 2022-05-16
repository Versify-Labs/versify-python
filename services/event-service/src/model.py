from pynamodb.attributes import (MapAttribute, NumberAttribute, UnicodeAttribute,
                                 VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel
import os


class ByObjectIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'byObjectId'
        projection = AllProjection()

    object_id = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)


class ByObjectTypeIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'byObjectType'
        projection = AllProjection()

    object_type = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True)


class Event(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']
        object_name = 'event'

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    merchant = UnicodeAttribute(hash_key=True, null=False)
    timestamp = NumberAttribute(range_key=True, null=False)
    object_id = UnicodeAttribute(null=False)
    object_id_index = ByObjectIdIndex()
    object_type = UnicodeAttribute(null=False)
    object_type_index = ByObjectTypeIndex()
    id = UnicodeAttribute(null=False)
    detail_type = UnicodeAttribute(null=False)
    detail = MapAttribute(null=False)
    merchant = UnicodeAttribute(null=True)
    source = UnicodeAttribute(null=False)
    version = VersionAttribute()
    wallet = UnicodeAttribute(null=True)
