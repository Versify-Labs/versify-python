from ..resources import Collection, Mint
from .errors import NotFoundError


class Signature:

    def __init__(self):
        self.object = 'signature'

    def exists(self, id: str):

        # Add signature id to query
        params = {'signature': id}

        # Check collections
        resource = Collection()
        collections = resource.find(params)

        # Check mints
        resource = Mint()
        mints = resource.find(params)

        if len(collections) + len(mints) > 0:
            return True
        raise NotFoundError
