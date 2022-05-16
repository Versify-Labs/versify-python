import os
import time

from pynamodb.attributes import (ListAttribute, MapAttribute, NumberAttribute,
                                 UnicodeAttribute, VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel

"""
Query Patterns
createAirdrop(network, name) => [PK=id, SK=id]
createOrder(collection, title, description, properties, image)
listOrdersByOrganization() => [PK=org, SK=object]
getOrder() => [PK=id, SK=id]
"""


class AirdropModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    customer = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    items = ListAttribute(null=False, default=[])
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='airdrop')
    organization = UnicodeAttribute(null=False)
    version = VersionAttribute()


class FulfillmentByEmailByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByEmailByObject'
        projection = AllProjection()

    email = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class FulfillmentByOrderByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrderByObject'
        projection = AllProjection()

    order = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class FulfillmentByOrganizationByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByObject'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class FulfillmentModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    blockchain_address = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    email = UnicodeAttribute(null=False)
    items = ListAttribute(null=False, default=[])
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='fulfillment')
    order = UnicodeAttribute(null=False)
    organization = UnicodeAttribute(null=False)
    status = UnicodeAttribute(null=False, default='unfulfilled')
    version = VersionAttribute()
    by_email_by_object = FulfillmentByEmailByObject()
    by_order_by_object = FulfillmentByOrderByObject()
    by_organization_by_object = FulfillmentByOrganizationByObject()


class OrderByEmailByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByEmailByObject'
        projection = AllProjection()

    email = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class OrderByOrganizationByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByObject'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class OrderModel(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    amount_currency = UnicodeAttribute(null=False, default="usd")
    amount_refunded = NumberAttribute(null=False, default=0)
    amount_shipping = NumberAttribute(null=False, default=0)
    amount_subtotal = NumberAttribute(null=False, default=0)
    amount_tax = NumberAttribute(null=False, default=0)
    amount_total = NumberAttribute(null=False, default=0)
    airdrop = UnicodeAttribute(null=True)
    billing_details = MapAttribute(null=False, default={})
    customer = UnicodeAttribute(null=False)
    customer_details = MapAttribute(null=False, default={})
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    email = UnicodeAttribute(null=False)
    fulfillment_status = UnicodeAttribute(null=False, default='unfulfilled')
    items = ListAttribute(null=False, default=[])
    merchant = UnicodeAttribute(null=False)
    merchant_details = MapAttribute(null=False, default={})
    metadata = MapAttribute(null=False, default={})
    object = UnicodeAttribute(null=False, default='order')
    organization = UnicodeAttribute(null=False)
    payment_status = UnicodeAttribute(null=False, default='unpaid')
    shipping_details = MapAttribute(null=False, default={})
    type = UnicodeAttribute(null=False)
    version = VersionAttribute()
    by_email_by_object = OrderByEmailByObject()
    by_organization_by_object = OrderByOrganizationByObject()
