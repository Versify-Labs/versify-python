from ..api.errors import NotFoundError


class SignatureService:

    def __init__(
        self,
        collection_service,
        mint_service
    ):
        self.object = 'signature'

        # Internal services
        self.collection_service = collection_service
        self.mint_service = mint_service

    def exists(self, id: str):

        # Add signature id to query
        filter = {'signature': id}

        # Check collections
        collections = self.collection_service.list(filter)

        # Check mints
        mints = self.mint_service.list(filter)

        if len(collections) + len(mints) > 0:
            return True

        raise NotFoundError
