from app.api.api_v1.endpoints import (
    assets,
    claims,
    collections,
    contacts,
    events,
    journeys,
    messages,
    mints,
    redemptions,
    rewards,
    users,
    webhooks,
)
from app.models.user import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter

from .auth import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

api_router = APIRouter()

# AUTHENTICATION
api_router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)
api_router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Authentication"],
)
api_router.include_router(
    router=fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Authentication"],
)
api_router.include_router(
    router=fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)
api_router.include_router(
    router=fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["Authentication"],
)
api_router.include_router(
    router=fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

# ENDPOINTS
# api_router.include_router(accounts.router)
# api_router.include_router(assets.router)
# api_router.include_router(claims.router)
# api_router.include_router(collections.router)
# api_router.include_router(contacts.router)
# api_router.include_router(events.router)
# api_router.include_router(journeys.router)
# api_router.include_router(messages.router)
# api_router.include_router(mints.router)
# api_router.include_router(redemptions.router)
# api_router.include_router(rewards.router)
# api_router.include_router(webhooks.router)
