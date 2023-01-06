from typing import List, Union

from app.models.account import Account
from app.models.globals import TeamMemberRole
from app.models.user import User
from fastapi import Body, Cookie, Header, Path, Query
from pydantic import BaseModel, Field, Required


class HTTPAuthorizationCredentials(BaseModel):
    scheme: str
    token: str


class Identity(BaseModel):
    user: Union[User, None] = None
    account: Union[Account, None] = None
    account_user_role: Union[TeamMemberRole, None] = None


class SearchQuery(BaseModel):
    query: str = Field(
        ...,
        description="The search query",
        example="NFT",
        title="Search Query",
    )
    page_num: int = Field(
        default=1,
        description="The page number",
        example=1,
        title="Page Number",
    )
    page_size: int = Field(
        default=10,
        description="The number of items per page",
        example=10,
        title="Per Page",
    )


class ApiDeleteResponse(BaseModel):
    id: str = Field(
        description="Unique identifier for the item",
        example="item_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    object: str = Field(
        default="item",
        description="The object type",
        example="item",
        title="Object Type",
    )
    deleted: bool = Field(
        default=True,
        description="Whether the item has been deleted",
        example=True,
        title="Deleted",
    )


class ApiListResponse(BaseModel):
    object: str = Field(
        default="list",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of items returned",
        example=1,
        title="Count",
    )
    data: List[Account] = Field(
        default=[],
        description="The list of items that match the filters and pagination parameters.",
        title="Accounts",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more items to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/items",
        description="The URL of the list request",
        example="/v1/items",
        title="URL",
    )


class ApiSearchResponse(BaseModel):
    object: str = Field(
        default="search_result",
        description="The object type",
        example="list",
        title="Object Type",
    )
    count: int = Field(
        default=0,
        description="The number of items returned",
        example=1,
        title="Count",
    )
    data: List[Account] = Field(
        default=[],
        description="The list of items that match the filters and pagination parameters.",
        title="Accounts",
    )
    has_more: bool = Field(
        default=False,
        description="Whether there are more items to be returned",
        example=False,
        title="Has More",
    )
    url: str = Field(
        default="/v1/items/search",
        description="The URL of the search request",
        example="/v1/items/search",
        title="URL",
    )


class BodyParams:
    CREATE_ACCOUNT = Body(
        default=Required,
        title="Account",
        description="Account to create",
        example={"domain": "acme.com", "name": "Acme Corp"},
    )
    CREATE_ASSET = Body(
        default=Required,
        title="Asset",
        description="Asset to create",
        example={
            "name": "Acme Corp",
            "description": "Acme Corp is a fictional company in the Looney Tunes universe.",
            "image": "https://acme.com/logo.png",
        },
    )
    CREATE_CONTACT = Body(
        default=Required,
        title="Contact",
        description="Contact to create",
    )
    CREATE_USER = Body(
        default=Required,
        title="User",
        description="User to create",
        example={"name": "Acme", "first_name": "Jane", "last_name": "Doe"},
    )
    SEARCH_CONTACTS = Body(
        default=Required,
        title="Search Contacts",
        description="Search contacts",
        examples={
            "Search with single filter": {
                "summary": "Search with single filter",
                "value": {
                    "query": {
                        "field": "email",
                        "operator": "contains",
                        "value": "acme.com",
                    }
                },
            },
            "Search with multiple filters": {
                "summary": "Search with multiple filters",
                "value": {
                    "query": {
                        "operator": "AND",
                        "value": [
                            {
                                "field": "email",
                                "operator": "contains",
                                "value": "acme.com",
                            },
                            {
                                "field": "name.first_name",
                                "operator": "contains",
                                "value": "Jane",
                            },
                        ],
                    }
                },
            },
            "Search with nested filters": {
                "summary": "Search with nested filters",
                "value": {
                    "query": {
                        "operator": "AND",
                        "value": [
                            {
                                "operator": "OR",
                                "value": [
                                    {
                                        "field": "created",
                                        "operator": ">",
                                        "value": 1560436650,
                                    },
                                    {
                                        "field": "created",
                                        "operator": ">",
                                        "value": 1560436784,
                                    },
                                ],
                            },
                            {
                                "operator": "AND",
                                "value": [
                                    {
                                        "field": "name.first_name",
                                        "operator": "!=",
                                        "value": None,
                                    },
                                    {
                                        "field": "name.last_name",
                                        "operator": "!=",
                                        "value": None,
                                    },
                                ],
                            },
                        ],
                    },
                },
            },
        },
    )
    UPDATE_ACCOUNT = Body(
        default=Required,
        title="Account",
        description="Account to update",
        example={
            "name": "Acme",
            "brand": {
                "primary_color": "#000000",
                "secondary_color": "#FFFFFF",
            },
            "domain": "acme.com",
        },
    )
    UPDATE_CONTACT = Body(
        default=Required,
        title="Contact",
        description="Contact to update",
        example={
            "name": {
                "first_name": "Jane",
                "last_name": "Doe",
            }
        },
    )
    UPDATE_USER = Body(
        default=Required,
        title="User",
        description="User to update",
        example={
            "avatar": "https://example.com/avatar.png",
            "name": {
                "first_name": "Jane",
                "last_name": "Doe",
            },
        },
    )


class CookieParams:
    SESSION_ID = Cookie(
        default=Required,
        title="Session ID",
        description="Session ID",
        example="5f4d7f4c6f4c6f4c6f4c6f4c",
    )


class HeaderParams:
    AUTHORIZATION = Header(
        alias="Authorization",
        default=None,
        regex="^Bearer .+",
        title="Authorization",
        description="Authorization",
        example="Bearer 5f4d7f4c6f4c6f4c6f4c6f4c",
    )
    CONTENT_TYPE = Header(
        default="application/json",
        title="Content Type",
        description="Content type header",
        example="application/json",
    )
    USER_AGENT = Header(
        default=None,
        title="User Agent",
        description="User agent header",
        example="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    )
    X_REQUEST_ID = Header(
        default=None,
        title="Request ID",
        description="Request ID header",
        example="req_1123123131231231",
    )
    VERSIFY_ACCOUNT = Header(
        default=Required,
        alias="Versify-Account",
        title="Versify Account",
        description="Versify Account",
        example="act_2323213123123123",
    )


class PathParams:
    ACCOUNT_ID = Path(
        default=Required,
        title="Account ID",
        description="Unique identifier of the account",
        example="act_2323213123123123",
    )
    CONTACT_ID = Path(
        default=Required,
        title="Contact ID",
        description="Unique identifier of the contact",
        example="con_12121231231231321",
    )
    USER_ID = Path(
        default=Required,
        title="User ID",
        description="Unique identifier of the user",
        example="usr_12121231231231321",
    )


class QueryParams:
    COLLECTION_ID = Query(
        default=None,
        title="Collection ID",
        description="Collection ID",
        example="col_12121231231231321",
    )
    COLLECTION_STATUS = Query(
        default=None,
        title="Collection Status",
        description="Collection status",
        example="active",
    )
    EXPAND = Query(
        default=None,
        title="Expand",
        description="Expand",
        example="contact",
    )
    OBJECT_TYPES = Query(
        default=None,
        title="Object Types",
        description="Object types",
        example="contact",
    )
    PAGE_NUM = Query(
        default=1,
        title="Page Number",
        description="Page number",
        example=1,
    )
    PAGE_SIZE = Query(
        default=10,
        title="Page Size",
        description="Page size",
        example=10,
    )
