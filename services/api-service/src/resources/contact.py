from .base import ApiResource


class Contact(ApiResource):

    def __init__(self):
        object = 'contact'
        super().__init__(object)
