from fastapi import APIRouter, Request

router = APIRouter(prefix="/mints", tags=["Mints"])


@router.post(
    path="",
    summary="Create an mint",
    description="Create an mint",
    tags=["Mints"],
    status_code=201,
    response_model=None,
    response_description="The created mint",
)
def create_mint(request: Request):
    """
    Create Mint
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List mints",
    description="List mints with optional filters and pagination parameters",
    tags=["Mints"],
    status_code=200,
    response_model=None,
    response_description="The list of mints",
)
def list_mints(request: Request):
    """
    List Mints
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{mint_id}",
    summary="Get an mint",
    description="Get an mint",
    tags=["Mints"],
    status_code=200,
    response_model=None,
    response_description="The mint",
)
def get_mint(request: Request):
    """
    Get Mint
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{mint_id}",
    summary="Update an mint",
    description="Update an mint",
    tags=["Mints"],
    status_code=200,
    response_model=None,
    response_description="The updated mint",
)
def update_mint(request: Request):
    """
    Update Mint
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{mint_id}",
    summary="Delete an mint",
    description="Delete an mint",
    tags=["Mints"],
    status_code=200,
    response_model=None,
    response_description="The deleted mint",
)
def delete_mint(request: Request):
    """
    Delete Mint
    """
    return {"message": "Not implemented"}
