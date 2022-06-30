from .base import ApiResource


class Airdrop(ApiResource):

    def __init__(self):
        object = 'airdrop'
        super().__init__(object)
