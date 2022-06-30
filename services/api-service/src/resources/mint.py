import os

from .base import ApiResource

ENVIRONMENT = os.environ['ENVIRONMENT']
if ENVIRONMENT == 'prod':
    MINT_URL = 'https://dashboard.versifylabs.com'
else:
    MINT_URL = 'https://dashboard-dev.versifylabs.com'


class Mint(ApiResource):

    def __init__(self):
        object = 'mint'
        super().__init__(object)

    def inject_data(self, raw):
        raw['url'] = MINT_URL + '/mint/' + raw['_id']
        return super().inject_data(raw)
