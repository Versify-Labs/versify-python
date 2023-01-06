from app.api.deps import identity_with_account
from app.crud import versify
from app.api.models import (
    ApiDeleteResponse,
    ApiListResponse,
    ApiSearchResponse,
    BodyParams,
    Identity,
    PathParams,
    QueryParams,
    SearchQuery,
)
from app.models.reward import Reward, RewardCreate, RewardUpdate

from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/rewards", tags=["Rewards"])


@router.get(
    path="",
    summary="List rewards",
    description="List rewards with optional filters and pagination parameters",
    tags=["Rewards"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of rewards",
)
def list_rewards(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.rewards.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    rewards = versify.rewards.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": rewards, "has_more": count > len(rewards)}


@router.post(
    path="/search",
    summary="Search rewards",
    description="Search rewards with query string",
    tags=["Rewards"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of rewards",
)
def search_rewards(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    rewards = versify.rewards.search(account=identity.account.id, query=query)
    return {"count": len(rewards), "data": rewards}


@router.post(
    path="",
    summary="Create reward",
    description="Create a reward",
    tags=["Rewards"],
    status_code=201,
    response_model=Reward,
    response_description="The created reward",
)
def create_reward(
    identity: Identity = Depends(identity_with_account),
    reward_create: RewardCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = reward_create.dict()
    body["account"] = identity.account.id
    create_result = versify.rewards.create(body)
    return create_result


@router.get(
    path="/{reward_id}",
    summary="Get reward",
    description="Get a reward",
    tags=["Rewards"],
    status_code=200,
    response_model=Reward,
    response_description="The reward",
)
def get_reward(
    identity: Identity = Depends(identity_with_account),
    reward_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward = versify.rewards.get(reward_id)
    if not reward:
        raise NotFoundException("Reward not found")
    if reward.account != identity.account.id:
        raise ForbiddenException()
    return reward


@router.put(
    path="/{reward_id}",
    summary="Update reward",
    description="Update an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=Reward,
    response_description="The updated reward",
)
def update_reward(
    identity: Identity = Depends(identity_with_account),
    reward_id: str = PathParams.CONTACT_ID,
    reward_update: RewardUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward = versify.rewards.get(reward_id)
    if not reward:
        raise NotFoundException()
    if reward.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.rewards.update(reward_id, reward_update.dict())
    return update_result


@router.delete(
    path="/{reward_id}",
    summary="Delete reward",
    description="Delete an reward",
    tags=["Rewards"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted reward",
)
def delete_reward(
    identity: Identity = Depends(identity_with_account),
    reward_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    reward = versify.rewards.get(reward_id)
    if not reward:
        raise NotFoundException()
    if reward.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.rewards.delete(reward_id)
    return delete_result
