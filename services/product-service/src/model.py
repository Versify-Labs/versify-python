import os
import time

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


class CollectionByOrganizationByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByObject'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class CollectionModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    # Updates to deployed contract address
    address = UnicodeAttribute(null=True)
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False)
    # Blockchain network to deploy the contract to
    network = UnicodeAttribute(null=False)
    object = UnicodeAttribute(null=False, default='collection')
    organization = UnicodeAttribute(null=False)
    # Changes to deployed once contract is deployed
    state = UnicodeAttribute(null=False, default='pending')
    symbol = UnicodeAttribute(null=False)
    tags = ListAttribute(null=False, default=[])
    # folder in s3 bucket that has subfolder for each token_id: https:://s3.aws.{bucket_name}}/{contract_uri}/
    token_uri = UnicodeAttribute(null=False)
    type = UnicodeAttribute(null=False)
    version = VersionAttribute()
    by_organization_by_object = CollectionByOrganizationByObject()


class ProductByOrganizationByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByObject'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class ProductModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    active = BooleanAttribute(null=False, default=True)
    # Optional field used by animated tokens. `image` is still required
    animation = UnicodeAttribute(null=True)
    contract_address = UnicodeAttribute(null=True)
    collection = UnicodeAttribute(null=False)
    collection_details = MapAttribute(null=False, default={})
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    # The number of decimal places that the token amount should display - e.g. 18, means to divide the token amount by 1000000000000000000 to get its user representation.
    decimals = NumberAttribute(null=False, default=18)
    # Describes the asset to which this NFT represents
    description = UnicodeAttribute(null=False)
    # A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents.
    # # Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive.
    # The URI value allows for ID substitution by clients.
    # If the string {id} exists in any URI, clients MUST replace this with the actual token ID in hexadecimal form.
    # This allows for a large number of tokens to use the same on-chain string by defining a URI once, for that large number of tokens.
    # The string format of the substituted hexadecimal ID MUST be lowercase alphanumeric: [0-9a-f] with no 0x prefix.
    # The string format of the substituted hexadecimal ID MUST be leading zero padded to 64 hex characters length if necessary.
    # Example: https://token-cdn-domain/{id}.json -> https://token-cdn-domain/000000000000000000000000000000000000000000000000000000000004cce0.json if the client is referring to token ID 314592/0x4CCE0.
    # Example: https://s3.amazonaws.com/versify-1155/{contract_address}/images/{id}.png"
    image = UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    # Identifies the asset to which this NFT represents
    name = UnicodeAttribute(null=False)
    object = UnicodeAttribute(null=False, default='product')
    organization = UnicodeAttribute(null=False)
    # Arbitrary properties. Values may be strings, numbers, object or arrays.
    properties = MapAttribute(null=False, default={})
    tags = ListAttribute(null=False, default=[])
    token_id = UnicodeAttribute(null=True)
    total_sold = NumberAttribute(null=False, default=0)
    total_supply = NumberAttribute(null=False, default=1)
    version = VersionAttribute()
    by_organization_by_object = ProductByOrganizationByObject()
