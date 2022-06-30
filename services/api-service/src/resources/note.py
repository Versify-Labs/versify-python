from .base import ApiResource


class Note(ApiResource):

    def __init__(self):
        object = 'note'
        super().__init__(object)
