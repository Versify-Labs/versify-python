from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.claim import (
    ClaimCreateRequest,
    ClaimCreateResponse,
    ClaimDeleteResponse,
    ClaimGetResponse,
    ClaimListRequest,
    ClaimListResponse,
    ClaimSearchRequest,
    ClaimSearchResponse,
    ClaimUpdateRequest,
    ClaimUpdateResponse,
)
from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.get(
    path="",
    summary="List claims",
    description="List claims with optional filters and pagination parameters",
    tags=["Claims"],
    status_code=200,
    response_model=ClaimListResponse,
    response_description="The list of claims",
)
def list_claims(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    claim_list_request: ClaimListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.claims.count(
        account=current_account.id,
    )
    claims = versify.claims.list(
        page_num=claim_list_request.page_num,
        page_size=claim_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": claims, "has_more": count > len(claims)}


@router.post(
    path="/search",
    summary="Search claims",
    description="Search claims with query string",
    tags=["Claims"],
    status_code=200,
    response_model=ClaimSearchResponse,
    response_description="The list of claims",
)
def search_claims(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    claim_search_request: ClaimSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim_search_request_dict = claim_search_request.dict()
    query = claim_search_request_dict["query"]
    claims = versify.claims.search(account=current_account.id, query=query)
    return {"count": len(claims), "data": claims}


@router.post(
    path="",
    summary="Create claim",
    description="Create a claim",
    tags=["Claims"],
    status_code=201,
    response_model=ClaimCreateResponse,
    response_description="The created claim",
)
def create_claim(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    claim_create: ClaimCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = claim_create.dict()
    body["account"] = current_account.id
    create_result = versify.claims.create(body)
    return create_result


@router.get(
    path="/{claim_id}",
    summary="Get claim",
    description="Get a claim",
    tags=["Claims"],
    status_code=200,
    response_model=ClaimGetResponse,
    response_description="The claim",
)
def get_claim(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    claim_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim = versify.claims.get(claim_id)
    if not claim:
        raise NotFoundException()
    if claim.account != current_account.id:
        raise ForbiddenException()
    return claim


@router.put(
    path="/{claim_id}",
    summary="Update claim",
    description="Update an claim",
    tags=["Claims"],
    status_code=200,
    response_model=ClaimUpdateResponse,
    response_description="The updated claim",
)
def update_claim(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    claim_id: str = PathParams.CONTACT_ID,
    claim_update: ClaimUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim = versify.claims.get(claim_id)
    if not claim:
        raise NotFoundException()
    if claim.account != current_account.id:
        raise ForbiddenException()
    body = claim_update.dict()
    update_result = versify.claims.update(claim_id, body)
    return update_result


@router.delete(
    path="/{claim_id}",
    summary="Delete claim",
    description="Delete an claim",
    tags=["Claims"],
    status_code=200,
    response_model=ClaimDeleteResponse,
    response_description="The deleted claim",
)
def delete_claim(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    claim_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim = versify.claims.get(claim_id)
    if not claim:
        raise NotFoundException()
    if claim.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.claims.delete(claim_id)
    return delete_result
