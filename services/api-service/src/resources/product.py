from .base import ApiResource


class Product(ApiResource):

    def __init__(self):
        object = 'product'
        super().__init__(object)
