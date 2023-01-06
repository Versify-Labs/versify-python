from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.reward import (
    RewardCreateRequest,
    RewardCreateResponse,
    RewardDeleteResponse,
    RewardGetResponse,
    RewardListRequest,
    RewardListResponse,
    RewardSearchRequest,
    RewardSearchResponse,
    RewardUpdateRequest,
    RewardUpdateResponse,
)
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/rewards", tags=["Rewards"])


@router.get(
    path="",
    summary="List rewards",
    description="List rewards with optional filters and pagination parameters",
    tags=["Rewards"],
    status_code=200,
    response_model=RewardListResponse,
    response_description="The list of rewards",
)
def list_rewards(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    reward_list_request: RewardListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.rewards.count(
        account=current_account.id,
    )
    rewards = versify.rewards.list(
        page_num=reward_list_request.page_num,
        page_size=reward_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": rewards, "has_more": count > len(rewards)}


@router.post(
    path="/search",
    summary="Search rewards",
    description="Search rewards with query string",
    tags=["Rewards"],
    status_code=200,
    response_model=RewardSearchResponse,
    response_description="The list of rewards",
)
def search_rewards(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    reward_search_request: RewardSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward_search_request_dict = reward_search_request.dict()
    query = reward_search_request_dict["query"]
    rewards = versify.rewards.search(account=current_account.id, query=query)
    return {"count": len(rewards), "data": rewards}


@router.post(
    path="",
    summary="Create reward",
    description="Create a reward",
    tags=["Rewards"],
    status_code=201,
    response_model=RewardCreateResponse,
    response_description="The created reward",
)
def create_reward(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    reward_create: RewardCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = reward_create.dict()
    body["account"] = current_account.id
    create_result = versify.rewards.create(body)
    return create_result


@router.get(
    path="/{reward_id}",
    summary="Get reward",
    description="Get a reward",
    tags=["Rewards"],
    status_code=200,
    response_model=RewardGetResponse,
    response_description="The reward",
)
def get_reward(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    reward_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward = versify.rewards.get(reward_id)
    if not reward:
        raise NotFoundException()
    if reward.account != current_account.id:
        raise ForbiddenException()
    return reward


@router.put(
    path="/{reward_id}",
    summary="Update reward",
    description="Update an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=RewardUpdateResponse,
    response_description="The updated reward",
)
def update_reward(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    reward_id: str = PathParams.CONTACT_ID,
    reward_update: RewardUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward = versify.rewards.get(reward_id)
    if not reward:
        raise NotFoundException()
    if reward.account != current_account.id:
        raise ForbiddenException()
    body = reward_update.dict()
    update_result = versify.rewards.update(reward_id, body)
    return update_result


@router.delete(
    path="/{reward_id}",
    summary="Delete reward",
    description="Delete an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=RewardDeleteResponse,
    response_description="The deleted reward",
)
def delete_reward(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    reward_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward = versify.rewards.get(reward_id)
    if not reward:
        raise NotFoundException()
    if reward.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.rewards.delete(reward_id)
    return delete_result
