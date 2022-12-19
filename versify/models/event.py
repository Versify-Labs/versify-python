from typing import Optional

from ._base import BaseAccountModel


class Event(BaseAccountModel):
    object: str = 'event'
    contact: Optional[str]
    detail_type: str
    detail: dict = {}
    source: str = 'versify'
