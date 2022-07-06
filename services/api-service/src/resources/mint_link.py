import os

from .base import ApiResource

ENVIRONMENT = os.environ['ENVIRONMENT']
if ENVIRONMENT == 'prod':
    MINT_URL = 'https://mint.versifylabs.com'
else:
    MINT_URL = 'https://mint-dev.versifylabs.com'


class MintLink(ApiResource):

    def __init__(self):
        object = 'mint_link'
        super().__init__(object)

    def inject_data(self, raw):
        raw['url'] = MINT_URL + '/link/' + raw['_id']
        return super().inject_data(raw)
