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
from app.models.claim import Claim, ClaimCreate, ClaimUpdate

from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.get(
    path="",
    summary="List claims",
    description="List claims with optional filters and pagination parameters",
    tags=["Claims"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of claims",
)
def list_claims(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.claims.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    claims = versify.claims.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": claims, "has_more": count > len(claims)}


@router.post(
    path="/search",
    summary="Search claims",
    description="Search claims with query string",
    tags=["Claims"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of claims",
)
def search_claims(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    claims = versify.claims.search(account=identity.account.id, query=query)
    return {"count": len(claims), "data": claims}


@router.post(
    path="",
    summary="Create claim",
    description="Create a claim",
    tags=["Claims"],
    status_code=201,
    response_model=Claim,
    response_description="The created claim",
)
def create_claim(
    identity: Identity = Depends(identity_with_account),
    claim_create: ClaimCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = claim_create.dict()
    body["account"] = identity.account.id
    create_result = versify.claims.create(body)
    return create_result


@router.get(
    path="/{claim_id}",
    summary="Get claim",
    description="Get a claim",
    tags=["Claims"],
    status_code=200,
    response_model=Claim,
    response_description="The claim",
)
def get_claim(
    identity: Identity = Depends(identity_with_account),
    claim_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim = versify.claims.get(claim_id)
    if not claim:
        raise NotFoundException("Claim not found")
    if claim.account != identity.account.id:
        raise ForbiddenException()
    return claim


@router.put(
    path="/{claim_id}",
    summary="Update claim",
    description="Update an claim",
    tags=["Claims"],
    status_code=200,
    response_model=Claim,
    response_description="The updated claim",
)
def update_claim(
    identity: Identity = Depends(identity_with_account),
    claim_id: str = PathParams.CONTACT_ID,
    claim_update: ClaimUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim = versify.claims.get(claim_id)
    if not claim:
        raise NotFoundException()
    if claim.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.claims.update(claim_id, claim_update.dict())
    return update_result


@router.delete(
    path="/{claim_id}",
    summary="Delete claim",
    description="Delete an claim",
    tags=["Claims"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted claim",
)
def delete_claim(
    identity: Identity = Depends(identity_with_account),
    claim_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    claim = versify.claims.get(claim_id)
    if not claim:
        raise NotFoundException()
    if claim.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.claims.delete(claim_id)
    return delete_result
