from app.api.deps import current_active_user
from app.crud import versify
from app.api.exceptions import ForbiddenException
from app.models.params import BodyParams, PathParams
from app.models.user import User, UserDeleted, UserUpdate
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/me",
    summary="Get current user",
    description="Get current user",
    status_code=200,
    response_model=User,
    response_description="The current user",
)
def get_current_user(user: User = Depends(current_active_user)):
    """
    Get Current User
    """
    return user


@router.put(
    path="/me",
    summary="Update current user",
    description="Update current user",
    status_code=200,
    response_model=User,
    response_description="The updated current user",
)
def update_current_user(
    current_user: User = Depends(current_active_user),
    user_update: UserUpdate = BodyParams.UPDATE_USER,
):
    """
    Update Current User
    """
    updated_user = versify.users.update(current_user.id, user_update.dict())
    return updated_user


@router.get(
    path="/{user_id}",
    summary="Get user",
    description="Get an user",
    status_code=200,
    response_model=User,
    response_description="The user",
)
def get_user(
    current_user: User = Depends(current_active_user),
    user_id: str = PathParams.USER_ID,
):
    """
    Get User
    """
    if current_user.id != user_id:
        raise ForbiddenException()
    return current_user


@router.put(
    path="/{user_id}",
    summary="Update user",
    description="Update an user",
    status_code=200,
    response_model=User,
    response_description="The updated user",
)
def update_user(
    current_user: User = Depends(current_active_user),
    user_id: str = PathParams.USER_ID,
    user_update: UserUpdate = BodyParams.UPDATE_USER,
):
    """
    Update User
    """
    if current_user.id != user_id:
        raise ForbiddenException()
    updated_user = versify.users.update(user_id, user_update.dict())
    return updated_user


@router.delete(
    path="/{user_id}",
    summary="Delete user",
    description="Delete an user",
    status_code=200,
    response_model=UserDeleted,
    response_description="The deleted user",
)
def delete_user(
    current_user: User = Depends(current_active_user),
    user_id: str = PathParams.USER_ID,
):
    """
    Delete User
    """
    if current_user.id != user_id:
        raise ForbiddenException()
    raise HTTPException(status_code=501, detail="Not implemented yet")
