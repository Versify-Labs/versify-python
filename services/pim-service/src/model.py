import os

from pynamodb.attributes import (BooleanAttribute, ListAttribute, MapAttribute, NumberAttribute,
                                 UnicodeAttribute, VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel

"""
Query Patterns
createCollection(network, name) => [PK=id, SK=id]
listCollectionsByOrganization() => [PK=org, SK=object]
getCollection() => [PK=id, SK=id]
createProduct(collection, title, description, properties, image)
listProductsByOrganization() => [PK=org, SK=object]
getProduct() => [PK=id, SK=id]
"""


class ListCollectionsByOrganization(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByDateCreated'
        projection = AllProjection()

    PK = UnicodeAttribute(hash_key=True)
    date_created = UnicodeAttribute(range_key=True)


class CollectionModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    active = BooleanAttribute(default=True)
    # contract: Updates to deployed contract address
    # contract_details.state:  Updates to deployed once contract is deployed
    # contract_details.token_uri: in s3 bucket that has subfolder for each token_id: https:://s3.aws.{bucket_name}}/{contract_uri}/
    contract = UnicodeAttribute(null=True)
    contract_details = MapAttribute(null=False, default={})
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    description = UnicodeAttribute(null=False, default='')
    image = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False)
    object = UnicodeAttribute(null=False, default='collection')
    organization = UnicodeAttribute(null=False)
    tags = ListAttribute(null=False, default=[])
    version = VersionAttribute()
    by_organization = ListCollectionsByOrganization()


class ListProductsByOrganization(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByObject'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class ProductModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(range_key=True, null=False)
    active = BooleanAttribute(default=True)
    collection = UnicodeAttribute(null=False)
    collection_details = MapAttribute(null=False, default={})
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    description = UnicodeAttribute(null=False)
    image = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False)
    object = UnicodeAttribute(null=False, default='product')
    organization = UnicodeAttribute(null=False)
    properties = ListAttribute(null=False, default=[])
    token = UnicodeAttribute(null=True)
    token_details = MapAttribute(null=False, default={})
    total_airdrops = NumberAttribute(null=False, default=0)
    total_sold = NumberAttribute(null=False, default=0)
    total_supply = NumberAttribute(null=False, default=1)
    version = VersionAttribute()
    by_organization = ListCollectionsByOrganization()
