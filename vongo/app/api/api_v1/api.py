from app.api.api_v1.endpoints import (accounts, assets, claims, collections,
                                      contacts, events, journeys, messages,
                                      mints, redemptions, rewards, users,
                                      webhooks)
from app.models.user import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter

from ..users import fastapi_users

api_router = APIRouter()

# AUTHENTICATION
SECRET = "SECRET"

# api_router.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["Authentication"]
# )
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Authentication"],
)

# @api_router.get("/authenticated-route")
# async def authenticated_route(user: User = Depends(current_active_user)):
#     return {"message": f"Hello {user.email}!"}

# @api_router.on_event("startup")
# async def on_startup():
#     await init_beanie(
#         database=db,
#         document_models=[
#             User,
#         ]
#     )

# ENDPOINTS
api_router.include_router(accounts.router)
api_router.include_router(assets.router)
api_router.include_router(claims.router)
api_router.include_router(collections.router)
api_router.include_router(contacts.router)
api_router.include_router(events.router)
api_router.include_router(journeys.router)
api_router.include_router(messages.router)
api_router.include_router(mints.router)
api_router.include_router(redemptions.router)
api_router.include_router(rewards.router)
api_router.include_router(users.router)
api_router.include_router(webhooks.router)
