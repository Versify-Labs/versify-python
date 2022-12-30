from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    path="",
    summary="Create an user",
    description="Create an user",
    tags=["Users"],
    status_code=201,
    response_model=None,
    response_description="The created user",
)
def create_user(
    request: Request
):
    """
    Create User
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List users",
    description="List users with optional filters and pagination parameters",
    tags=["Users"],
    status_code=200,
    response_model=None,
    response_description="The list of users",
)
def list_users(
    request: Request
):
    """
    List Users
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{user_id}",
    summary="Get an user",
    description="Get an user",
    tags=["Users"],
    status_code=200,
    response_model=None,
    response_description="The user",
)
def get_user(
    request: Request
):
    """
    Get User
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{user_id}",
    summary="Update an user",
    description="Update an user",
    tags=["Users"],
    status_code=200,
    response_model=None,
    response_description="The updated user",
)
def update_user(
    request: Request
):
    """
    Update User
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{user_id}",
    summary="Delete an user",
    description="Delete an user",
    tags=["Users"],
    status_code=200,
    response_model=None,
    response_description="The deleted user",
)
def delete_user(
    request: Request
):
    """
    Delete User
    """
    return {"message": "Not implemented"}
