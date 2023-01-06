from fastapi import APIRouter

from .endpoints import (
    accounts,
    assets,
    claims,
    collections,
    contacts,
    events,
    journeys,
    messages,
    mints,
    notes,
    redemptions,
    rewards,
    tags,
    users,
    webhooks,
)

api_router = APIRouter()
api_router.include_router(accounts.router)
api_router.include_router(assets.router)
api_router.include_router(claims.router)
api_router.include_router(collections.router)
api_router.include_router(contacts.router)
api_router.include_router(events.router)
api_router.include_router(journeys.router)
api_router.include_router(messages.router)
api_router.include_router(mints.router)
api_router.include_router(notes.router)
api_router.include_router(redemptions.router)
api_router.include_router(rewards.router)
api_router.include_router(tags.router)
api_router.include_router(users.router)
api_router.include_router(webhooks.router)
