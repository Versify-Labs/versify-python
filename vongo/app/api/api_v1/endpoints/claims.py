from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)


@router.post(
    path="",
    summary="Create an claim",
    description="Create an claim",
    tags=["Claims"],
    status_code=201,
    response_model=None,
    response_description="The created claim",
)
def create_claim(
    request: Request
):
    """
    Create Claim
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List claims",
    description="List claims with optional filters and pagination parameters",
    tags=["Claims"],
    status_code=200,
    response_model=None,
    response_description="The list of claims",
)
def list_claims(
    request: Request
):
    """
    List Claims
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{claim_id}",
    summary="Get an claim",
    description="Get an claim",
    tags=["Claims"],
    status_code=200,
    response_model=None,
    response_description="The claim",
)
def get_claim(
    request: Request
):
    """
    Get Claim
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{claim_id}",
    summary="Update an claim",
    description="Update an claim",
    tags=["Claims"],
    status_code=200,
    response_model=None,
    response_description="The updated claim",
)
def update_claim(
    request: Request
):
    """
    Update Claim
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{claim_id}",
    summary="Delete an claim",
    description="Delete an claim",
    tags=["Claims"],
    status_code=200,
    response_model=None,
    response_description="The deleted claim",
)
def delete_claim(
    request: Request
):
    """
    Delete Claim
    """
    return {"message": "Not implemented"}
