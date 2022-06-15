import os

from pynamodb.attributes import (MapAttribute, NumberAttribute,
                                 UnicodeAttribute, VersionAttribute)
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from versify.utilities.model import PlatformModel


class ListAirdropsByOrganization(GlobalSecondaryIndex):
    class Meta:
        index_name = 'GSI1'
        projection = AllProjection()

    GSI1PK = UnicodeAttribute(hash_key=True)           # org_123:airdrop
    GSI1SK = NumberAttribute(range_key=True)           # date_created


class ListAirdropsByCampaign(GlobalSecondaryIndex):
    class Meta:
        index_name = 'GSI2'
        projection = AllProjection()

    GSI2PK = UnicodeAttribute(hash_key=True)           # campaign_123:airdrop
    GSI2SK = NumberAttribute(range_key=True)           # date_created


class Airdrop(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)   # airdrop_123
    GSI1PK = UnicodeAttribute(null=False)              # org_123:airdrop
    GSI1SK = NumberAttribute(null=False)               # date_created
    GSI2PK = UnicodeAttribute(null=False)              # campaign_123:airdrop
    GSI2SK = NumberAttribute(null=False)               # date_created
    id = UnicodeAttribute(null=False)
    campaign = UnicodeAttribute(null=False)
    campaign_details = MapAttribute(null=False, default={})
    contact = UnicodeAttribute(null=False)
    contact_details = MapAttribute(null=False, default={})
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    # mint_details.address: Blockchain address that was used to fulfill the airdrop
    # mint_details.date_minted: Date of the mint
    # mint_details.email: Email of the user who claimed the mint
    # mint_details.link: URL that can be used to fulfill the airdrop claim
    # mint_details.txn: Transaction hash of the mint
    mint = UnicodeAttribute(null=True)
    mint_details = MapAttribute(null=False, default=True)
    object = UnicodeAttribute(null=False, default='airdrop')
    organization = UnicodeAttribute(null=False)
    organization_details = MapAttribute(null=False, default={})
    product = UnicodeAttribute(null=False)
    product_details = MapAttribute(null=False, default={})
    # Defaults to open, changes to pending -> closed
    status = UnicodeAttribute(null=False, default='open')
    version = VersionAttribute()
    by_campaign = ListAirdropsByCampaign()
    by_organization = ListAirdropsByCampaign()


class ListCampaignsByOrganization(GlobalSecondaryIndex):
    class Meta:
        index_name = 'GSI1'
        projection = AllProjection()

    GSI1PK = UnicodeAttribute(hash_key=True)           # org_123:campaign
    GSI1SK = NumberAttribute(range_key=True)           # date_created


class Campaign(PlatformModel):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    PK = UnicodeAttribute(hash_key=True, null=False)   # campaign_123
    GSI1PK = UnicodeAttribute(null=False)              # org_123:campaign
    GSI1SK = NumberAttribute(null=False)               # date_created
    GSI2PK = UnicodeAttribute(null=False)              # org_123:campaign
    GSI2SK = NumberAttribute(null=False)               # date_created
    id = UnicodeAttribute(null=False)
    date_created = NumberAttribute(null=False)
    date_updated = NumberAttribute(null=False)
    email_settings = MapAttribute(null=False, default={})
    # email_settings.content = UnicodeAttribute(null=False)
    # email_settings.from_email: UnicodeAttribute(null=False)
    # email_settings.from_: UnicodeAttribute(null=False)
    # email_settings.from_name: UnicodeAttribute(null=False)
    # email_settings.preview_text: UnicodeAttribute(null=False)
    # email_settings.subject_line: UnicodeAttribute(null=False)
    metadata = MapAttribute(null=False, default={})
    name = UnicodeAttribute(null=False, default="")
    object = UnicodeAttribute(null=False, default='campaign')
    organization = UnicodeAttribute(null=False)
    organization_details = MapAttribute(null=False, default={})
    product = UnicodeAttribute(null=False)
    product_details = MapAttribute(null=False, default={})
    # recipients.count: Count of the recipients of the associated segment options. Saved on create/update
    # recipients.segment: ID for a saved segment
    # recipients.segment_options.match: segment match type ("any" or "all")
    # recipients.segment_options.conditions: segment match condition (ex: email-equals-jane@example.com' || tags-include)
    recipients = MapAttribute(null=False, default={})
    # Defaults to draft, changes to sending -> complete
    results = MapAttribute(null=False, default={})
    status = UnicodeAttribute(null=False, default='draft')
    type = UnicodeAttribute(null=False, default='airdrop')
    version = VersionAttribute()
    by_organization = ListCampaignsByOrganization()
