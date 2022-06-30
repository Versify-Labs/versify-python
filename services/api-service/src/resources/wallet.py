from .base import ApiResource


class Wallet(ApiResource):

    def __init__(self):
        object = 'wallet'
        super().__init__(object)
