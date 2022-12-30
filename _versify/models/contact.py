from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from ._base import BaseAccountModel


class Note(BaseModel):
    id: str
    object = 'note'
    created: int
    content: str = ''
    user: dict = {}


class Contact(BaseAccountModel):
    id: Optional[str] = Field(None, alias="_id")
    object = 'contact'
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    created: int
    currency: str = 'usd'
    description: str = ''
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    metadata: Optional[dict] = {}
    name: Optional[str]
    notes: list[Note] = []
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []
    updated: Optional[int]
    wallet_address: Optional[str]


class ContactCreateRequest(BaseModel):
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    currency: str = 'usd'
    description: str = ''
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    notes: list[Note] = []
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []


class ContactUpdateRequest(BaseModel):
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    currency: str = 'usd'
    description: str = ''
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    notes: list[Note] = []
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []


class ContactResponse(BaseModel):
    id: str
    active: bool = True
    address: Optional[dict]
    avatar: Optional[str]
    balance: int = 0
    created: int
    currency: str = 'usd'
    description: str = ''
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    notes: list[Note] = []
    phone: Optional[str]
    shipping: Optional[dict]
    source: str = 'Versify'
    tags: list = []
    updated: int


class ContactDeletedResponse(BaseModel):
    id: str
    object: str = 'contact'
    deleted: bool = True


class ContactListQuery(BaseModel):
    active: Optional[bool]
    currency: Optional[str]
    email: Optional[EmailStr]
    expand: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    tags: Optional[list]
    limit: Optional[int]
    starting_after: Optional[str]
    ending_before: Optional[str]


class ContactListFilter(BaseModel):
    active: Optional[bool]
    currency: Optional[str]
    email: Optional[EmailStr]
    expand: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    source: Optional[str]
    tags: Optional[list]
    limit: Optional[int]
    starting_after: Optional[str]
    ending_before: Optional[str]


class ContactListResponse(BaseModel):
    object: str = 'list'
    url: str = '/v2/contacts'
    has_more: bool = False
    data: list = []
    count: Optional[int]


def get_response_model(role: str):
    if role == 'create':
        return ContactResponse
    elif role == 'update':
        return ContactResponse
    elif role == 'delete':
        return ContactDeletedResponse
    elif role == 'list':
        return ContactListResponse
    else:
        return ContactResponse
