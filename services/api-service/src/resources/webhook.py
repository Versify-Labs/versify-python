from .base import ApiResource


class Webhook(ApiResource):

    def __init__(self):
        object = 'webhook'
        super().__init__(object)
