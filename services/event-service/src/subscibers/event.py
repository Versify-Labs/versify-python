from ..utils.api import call_api
from ._base import BaseSubscriber


class EventSubscriber(BaseSubscriber):

    def start(self, event):
        payload = {
            'data': event.detail,
            'type': event.detail_type
        }
        return call_api(
            method='POST',
            path='/internal/events',
            body=payload
        )
