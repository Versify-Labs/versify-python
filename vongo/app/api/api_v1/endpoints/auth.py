# from typing import Union

# from app.crud import versify
# from fastapi import APIRouter, Body, Depends, Query, status

# from ...deps import get_current_user

# router = APIRouter(
#     prefix="/v2/oauth",
#     tags=["Authentication"]
# )


# @router.get('/register', status_code=status.HTTP_200_OK)
# async def register():
#     return {"message": "Not implemented"}


# @router.get('/login', status_code=status.HTTP_200_OK)
# async def login():
#     return {"message": "Not implemented"}


# @router.get(
#     path="/authorize",
#     summary="Authorize",
#     description="Authorize",
#     status_code=status.HTTP_200_OK,
#     response_description="The access code",
# )
# async def authorize(
#     client_id: str = Query(
#         ...,
#         title="Client ID",
#         description="The client ID for your application. You can find this value in your account settings page.",
#         example="pk_1234567890",
#     ),
#     redirect_uri: str = Query(
#         ...,
#         title="Redirect URI",
#         description="Determines where the API server redirects the user after the user completes the authorization flow.",
#         example="https://example.com/callback",
#     ),
#     response_type: str = Query(
#         ...,
#         title="Response type",
#         description="Determines whether the Versify OAuth 2.0 endpoint returns an authorization code. Set the value to code.",
#         example="code",
#     ),
#     scope: str = Query(
#         ...,
#         title="Scope",
#         description="A space-delimited list of scopes that identify the resources that your application could access on the user's behalf. These values inform the consent screen that Google displays to the user.",
#         example="read write",
#     ),
#     state: Union[str, None] = Query(
#         default=None,
#         title="State",
#         description="Specifies any string value that your application uses to maintain state between your authorization request and the authorization server's response.",
#         example="1234567890",
#     ),
# ):
#     return {"message": "Not implemented"}


# @router.post(
#     path="/token",
#     summary="Create access token",
#     description="This endpoint uses your Versify API Public Key and API Secret Key to generate the access_token necessary to authenticate most of Versify's API calls.",
#     status_code=status.HTTP_200_OK,
#     response_description="The access token",
# )
# async def create_access_token(
#     client_id: str = Body(
#         ...,
#         title="Client ID",
#         description="Also referred to as API public key.",
#         example="pk_1234567890",
#     ),
#     client_secret: str = Body(
#         ...,
#         title="Client secret",
#         description="Also referred to as API secret key.",
#         example="sk_1234567890",
#     ),
#     grant_type: str = Body(
#         ...,
#         title="Grant type",
#         description="Must be client_credentials",
#         example="client_credentials",
#     ),
# ):
#     return {"message": "Not implemented"}


# @router.get(
#     path="/user_info",
#     summary="User info",
#     description="User info",
#     status_code=status.HTTP_200_OK,
#     response_description="The user info embedded in the access token",
#     response_model=User,
# )
# async def get_user_info(
#     user: User = Depends(get_current_user)
# ):
#     return user


# @router.put(
#     path="/user_info",
#     summary="Update user info",
#     description="Update user info",
#     status_code=status.HTTP_200_OK,
#     response_description="The updated user info",
#     response_model=User,
# )
# async def update_user_info(
#     user: User = Depends(get_current_user),
#     user_update: UserUpdate = Body(
#         ...,
#         title="User update",
#         description="The user update",
#     ),
# ):
#     updated_user = versify.update_user(user.id, user_update.dict())
#     if not updated_user:
#         return status.HTTP_404_NOT_FOUND
#     return updated_user
