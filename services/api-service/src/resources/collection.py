from .base import ApiResource


class Collection(ApiResource):

    def __init__(self):
        object = 'collection'
        super().__init__(object)
