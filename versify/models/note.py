from typing import Optional

from ._base import BaseAccountModel


class Note(BaseAccountModel):
    object: str = 'note'
    attachment: Optional[str]
    content: str = ''
    resource_id: str
    resource_type: str
    user: dict
