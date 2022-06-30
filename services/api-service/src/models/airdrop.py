from .base import BaseCampaign


class Airdrop(BaseCampaign):
    object: str = 'airdrop'
    email_settings: dict = {}
    # email_settings.content
    # email_settings.from_email
    # email_settings.from_
    # email_settings.from_name
    # email_settings.preview_text
    # email_settings.subject_line
    name: str
    product: str
    recipients: dict = {
        'count': 0,
        'segment_options': {
            'conditions': '',
            'match': 'all'
        }
    }
    # recipients.count: Count of the recipients of the associated segment options. Saved on create/update (NOT IMPLEMENTED)
    # recipients.segment: ID for a saved segment (NOT IMPLEMENTED)
    # recipients.segment_options.match: segment match type ("any" or "all") (NOT IMPLEMENTED)
    # recipients.segment_options.conditions: segment match condition (ex: 'tags-$in-test')
    status: str = 'draft'  # changes to sending -> complete
