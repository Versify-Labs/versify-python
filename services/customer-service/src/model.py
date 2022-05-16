import os
import time

from pynamodb.attributes import (ListAttribute, MapAttribute, NumberAttribute,
                                 UnicodeAttribute, VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel

"""
Query Patterns
createCustomer(pk=id, sk=id)
getCustomer(pk=id, sk=id)
listCustomersByOrganization(pk=org, sk=object)
listCustomersByOrganizationByEmail(pk=org, sk=email)
"""


class ByOrganizationByEmail(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByEmail'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute(range_key=True)


class ByOrganizationByObject(GlobalSecondaryIndex):
    class Meta:
        index_name = 'ByOrganizationByObject'
        projection = AllProjection()

    organization = UnicodeAttribute(hash_key=True)
    object = UnicodeAttribute(range_key=True)


class Customer(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)
    SK = UnicodeAttribute(range_key=True, null=False)
    id = UnicodeAttribute(null=False)
    billing_addresses = ListAttribute(null=False, default=[])
    blockchain_addresses = ListAttribute(null=False, default=[])
    currency = UnicodeAttribute(null=False, default='usd')
    date_created = NumberAttribute(null=False, default=int(time.time()))
    date_updated = NumberAttribute(null=False, default=int(time.time()))
    description = UnicodeAttribute(null=False, default='')
    email = UnicodeAttribute(null=False)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=True)
    notes = UnicodeAttribute(null=False, default='')
    object = UnicodeAttribute(null=False, default='customer')
    organization = UnicodeAttribute(null=False)
    phone = UnicodeAttribute(null=True)
    shipping_addresses = ListAttribute(null=False, default=[])
    tags = ListAttribute(null=False, default=[])
    total_orders = NumberAttribute(null=False, default=0)
    total_spent = NumberAttribute(null=False, default=0)
    version = VersionAttribute()
    by_organization_by_email = ByOrganizationByEmail()
    by_organization_by_object = ByOrganizationByObject()
