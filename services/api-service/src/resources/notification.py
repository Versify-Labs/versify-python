from .base import ApiResource


class Notification(ApiResource):

    def __init__(self):
        object = 'notification'
        super().__init__(object)
