from beanie import PydanticObjectId
from fastapi_users import schemas
from fastapi_users.db import BeanieBaseUser
# from typing import Any, Dict, List, Optional, Union

# from pydantic import BaseModel, EmailStr, Field, root_validator

# from ..models.base import Base
# from ..models.factory import current_timestamp, generate_avatar, user_id
# from ..models.globals import IdentityProvider, PersonName, Wallet
# from .base import Base


class User(BeanieBaseUser[PydanticObjectId]):
    pass


class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# class UserBase(BaseModel):
#     email: Optional[EmailStr] = Field(
#         ...,
#         description='The email address of the user',
#     )
#     name: PersonName = Field(
#         default=PersonName(),
#         description='The name of the user',
#         title='Name'
#     )


# # Properties to receive via API on creation
# class UserCreate(UserBase):
#     email: EmailStr


# # Properties to receive via API on update
# class UserUpdate(UserBase):
#     avatar: Union[str, None] = Field(
#         default=None,
#         description='The URL of the user\'s avatar',
#         example='https://example.com/avatar.png',
#         title='Avatar URL'
#     )
#     name: Union[PersonName, None] = Field(
#         default=None,
#         description='The name of the user',
#         title='Name'
#     )
#     phone_number: Union[str, None] = Field(
#         default=None,
#         description='The phone number of the user',
#         example='+15555555555',
#         title='Phone Number'
#     )
#     updated: int = Field(
#         default_factory=current_timestamp,
#         description='The timestamp when the user was last updated',
#         example=1601059200,
#         title='Updated Timestamp'
#     )


# class UserInDBBase(UserBase):
#     id: Optional[int] = None

#     class Config:
#         orm_mode = True


# # Additional properties to return via API
# class User(Base):
#     id: str = Field(
#         alias="_id",
#         default_factory=user_id,
#         description='Unique identifier for the user',
#         example='user_5f9f1c5b0b9b4b0b9c1c5b0b',
#         title='User ID'
#     )
#     object: str = Field(
#         default='user',
#         description='The object type. Always "user"',
#         example='user',
#         title='Object Type'
#     )
#     active: bool = Field(
#         default=True,
#         description='Whether the user is active',
#         example=True,
#         title='Active'
#     )
#     avatar: str = Field(
#         ...,
#         description='The URL of the user\'s avatar',
#         example='https://example.com/avatar.png',
#         title='Avatar URL'
#     )
#     created: int = Field(
#         default_factory=current_timestamp,
#         description='The timestamp when the user was created',
#         example=1601059200,
#         title='Created Timestamp'
#     )
#     email: str = Field(
#         ...,
#         description='The email address of the user',
#         example='jane@example.com',
#         title='Email Address'
#     )
#     email_verified: bool = Field(
#         default=False,
#         description='Whether the user\'s email address has been verified',
#         example=True,
#         title='Email Verified'
#     )
#     metadata: Dict[str, Any] = Field(
#         default={},
#         description='Arbitrary metadata associated with the user',
#         example={'key': 'value'},
#         title='Metadata'
#     )
#     name: PersonName = Field(
#         default=PersonName(),
#         description='The name of the user',
#         title='Name'
#     )
#     phone_number: Union[str, None] = Field(
#         default=None,
#         description='The phone number of the user',
#         example='+15555555555',
#         title='Phone Number'
#     )
#     phone_number_verified: bool = Field(
#         default=False,
#         description='Whether the user\'s phone number has been verified',
#         example=True,
#         title='Phone Number Verified'
#     )
#     providers: List[IdentityProvider] = Field(
#         default=[],
#         description='The identity providers the user belongs to',
#         title='Identity Providers'
#     )
#     updated: int = Field(
#         default_factory=current_timestamp,
#         description='The timestamp when the user was last updated',
#         example=1601059200,
#         title='Updated Timestamp'
#     )
#     wallets: List[Wallet] = Field(
#         default=[Wallet(managed=True)],
#         description='The wallets the user belongs to',
#         title='Wallets'
#     )

#     @root_validator(pre=True)
#     def default_values(cls, values):
#         values['email'] = values['email'].lower()
#         if 'avatar' not in values:
#             values['avatar'] = generate_avatar(values['email'])
#         return values
