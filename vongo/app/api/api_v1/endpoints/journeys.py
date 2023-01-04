from fastapi import APIRouter, Request

router = APIRouter(prefix="/journeys", tags=["Journeys"])


@router.post(
    path="",
    summary="Create an journey",
    description="Create an journey",
    tags=["Journeys"],
    status_code=201,
    response_model=None,
    response_description="The created journey",
)
def create_journey(request: Request):
    """
    Create Journey
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List journeys",
    description="List journeys with optional filters and pagination parameters",
    tags=["Journeys"],
    status_code=200,
    response_model=None,
    response_description="The list of journeys",
)
def list_journeys(request: Request):
    """
    List Journeys
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{journey_id}",
    summary="Get an journey",
    description="Get an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=None,
    response_description="The journey",
)
def get_journey(request: Request):
    """
    Get Journey
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{journey_id}",
    summary="Update an journey",
    description="Update an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=None,
    response_description="The updated journey",
)
def update_journey(request: Request):
    """
    Update Journey
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{journey_id}",
    summary="Delete an journey",
    description="Delete an journey",
    tags=["Journeys"],
    status_code=200,
    response_model=None,
    response_description="The deleted journey",
)
def delete_journey(request: Request):
    """
    Delete Journey
    """
    return {"message": "Not implemented"}
