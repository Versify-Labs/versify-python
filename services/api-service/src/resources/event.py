from .base import ApiResource


class Event(ApiResource):

    def __init__(self):
        object = 'event'
        super().__init__(object)
