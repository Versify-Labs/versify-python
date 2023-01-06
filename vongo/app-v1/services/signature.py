from ..utils.exceptions import NotFoundError


class SignatureService:
    def __init__(self, collection_service, mint_service):
        self.object = "signature"

        # Internal services
        self.collection_service = collection_service
        self.mint_service = mint_service

    def exists(self, id: str) -> bool:
        """
        Check if a signature exists

        :param id: Signature id
        :type id: str
        :return: True if signature exists
        :rtype: bool
        """

        # Add signature id to query
        filter = {"signature": id}

        # Check collections
        collections = self.collection_service.list(filter)

        # Check mints
        mints = self.mint_service.list(filter)

        return len(collections) + len(mints) > 0
