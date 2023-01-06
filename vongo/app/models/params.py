from fastapi import Body, Cookie, Header, Path, Query


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
    )
    CREATE_USER = Body(
        ...,
        title="User",
        description="User to create",
        example={"name": "Acme", "first_name": "Jane", "last_name": "Doe"},
    )
    SEARCH_CONTACTS = Body(
        ...,
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
        ...,
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
        ...,
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
        ...,
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
        ...,
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
        ...,
        alias="Versify-Account",
        title="Versify Account",
        description="Versify Account",
        example="act_2323213123123123",
        
    )


class PathParams:
    ACCOUNT_ID = Path(
        ...,
        title="Account ID",
        description="Unique identifier of the account",
        example="act_2323213123123123",
    )
    CONTACT_ID = Path(
        ...,
        title="Contact ID",
        description="Unique identifier of the contact",
        example="con_12121231231231321",
    )
    USER_ID = Path(
        ...,
        title="User ID",
        description="Unique identifier of the user",
        example="usr_12121231231231321",
    )


class QueryParams:
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
