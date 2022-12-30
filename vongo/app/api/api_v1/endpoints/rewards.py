from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/rewards",
    tags=["Rewards"]
)


@router.post(
    path="",
    summary="Create an reward",
    description="Create an reward",
    tags=["Rewards"],
    status_code=201,
    response_model=None,
    response_description="The created reward",
)
def create_reward(
    request: Request
):
    """
    Create Reward
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List rewards",
    description="List rewards with optional filters and pagination parameters",
    tags=["Rewards"],
    status_code=200,
    response_model=None,
    response_description="The list of rewards",
)
def list_rewards(
    request: Request
):
    """
    List Rewards
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{reward_id}",
    summary="Get an reward",
    description="Get an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=None,
    response_description="The reward",
)
def get_reward(
    request: Request
):
    """
    Get Reward
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{reward_id}",
    summary="Update an reward",
    description="Update an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=None,
    response_description="The updated reward",
)
def update_reward(
    request: Request
):
    """
    Update Reward
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{reward_id}",
    summary="Delete an reward",
    description="Delete an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=None,
    response_description="The deleted reward",
)
def delete_reward(
    request: Request
):
    """
    Delete Reward
    """
    return {"message": "Not implemented"}
