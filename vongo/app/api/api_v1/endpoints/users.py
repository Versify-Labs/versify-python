from ...deps import identity
from ...exceptions import ForbiddenException
from ...models import BodyParams, Identity
from app.crud import versify
from app.models.user import User, UserUpdate
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/me",
    summary="Get current user",
    description="Get current user",
    status_code=200,
    response_model=User,
    response_description="The current user",
)
def get_current_user(identity: Identity = Depends(identity)):
    """
    Get Current User
    """
    return identity.user


@router.put(
    path="/me",
    summary="Update current user",
    description="Update current user",
    status_code=200,
    response_model=User,
    response_description="The updated current user",
)
def update_current_user(
    identity: Identity = Depends(identity),
    user_update: UserUpdate = BodyParams.UPDATE_USER,
):
    """
    Update Current User
    """
    if not identity.user:
        raise ForbiddenException()
    updated_user = versify.users.update(identity.user.id, user_update.dict())
    return updated_user
