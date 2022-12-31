"""Metadata for the Vongo API."""
from enum import Enum
from typing import Union

from fastapi import Body, Cookie, Header, Path, Query


class Tags(Enum):
    AUTHENTICATION = "Authentication"
    ACCOUNT = "Account"
    CONTACT = "Contact"


class BodyParams:
    CREATE_ACCOUNT = Body(
        ...,
        title="Account",
        description="Account to create",
        example={"domain": "acme.com", "name": "Acme Corp"},
    )
    CREATE_CONTACT = Body(
        ...,
        title="Contact",
        description="Contact to create",
        example={"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe"},
    )
    CREATE_USER = Body(
        ...,
        title="User",
        description="User to create",
        example={"name": "Acme", "first_name": "Jane", "last_name": "Doe"},
    )
    UPDATE_ACCOUNT = Body(
        ...,
        title="Account",
        description="Account to update",
        example={
            "name": "Acme",
        },
    )
    UPDATE_CONTACT = Body(
        ...,
        title="Contact",
        description="Contact to update",
        example={"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe"},
    )
    UPDATE_USER = Body(
        ...,
        title="User",
        description="User to update",
        example={
            "avatar": "https://example.com/avatar.png",
            "first_name": "Jane",
            "last_name": "Doe",
        },
    )


class CookieParams:
    SESSION_ID = Cookie(
        ..., title="Session ID", description="ID of the session", example="sess_1"
    )


class HeaderParams:
    AUTHORIZATION = Header(
        default=None,
        title="Authorization",
        description="Authorization header",
        example="Bearer ey......",
    )
    CONTENT_TYPE = Header(
        ...,
        title="Content Type",
        description="Content type header",
        example="application/json",
    )
    USER_AGENT = Header(
        ...,
        title="User Agent",
        description="User agent header",
        example="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    )
    X_REQUEST_ID = Header(
        ...,
        title="Request ID",
        description="Request ID header",
        example="req_1",
    )


class PathParams:
    ACCOUNT_ID = Path(
        ..., title="Account ID", description="ID of the account", example="acct_1"
    )
    CONTACT_ID = Path(
        ..., title="Contact ID", description="ID of the contact", example="cont_1"
    )
    USER_ID = Path(..., title="User ID", description="ID of the user", example="user_1")


class QueryParams:
    ACTIVE = Query(
        default=None,
        title="Active",
        description="Whether the item is active",
        example=True,
    )
    EMAIL = Query(
        default=None,
        title="Email",
        description="Email of the item to return",
        example="jane@example.com",
    )
    LIMIT = Query(
        default=10,
        ge=1,
        le=100,
        title="Limit amount",
        description="Number of items to return",
        example=10,
    )
    SKIP = Query(
        default=0,
        ge=0,
        title="Skip amount",
        description="Number of items to skip",
        example=10,
    )
    Q = Query(
        default=None,
        title="Search query",
        description="Query to filter items",
        example="Acme",
        min_length=1,
        max_length=100,
    )


class ListQueryParams:
    def __init__(self, limit: int = 100, skip: int = 0, q: Union[str, None] = None):
        self.limit = limit
        self.skip = skip
        self.q = q


tags_metadata = [
    {
        "name": Tags.AUTHENTICATION.value,
        "description": "Operations related to authentication.",
    },
    {"name": Tags.ACCOUNT.value, "description": "Operations with accounts."},
    {"name": Tags.CONTACT.value, "description": "Operations with contacts."},
]
