from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post(
    path="",
    summary="Create an webhook",
    description="Create an webhook",
    tags=["Webhooks"],
    status_code=201,
    response_model=None,
    response_description="The created webhook",
)
def create_webhook(
    request: Request
):
    """
    Create Webhook
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List webhooks",
    description="List webhooks with optional filters and pagination parameters",
    tags=["Webhooks"],
    status_code=200,
    response_model=None,
    response_description="The list of webhooks",
)
def list_webhooks(
    request: Request
):
    """
    List Webhooks
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{webhook_id}",
    summary="Get an webhook",
    description="Get an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=None,
    response_description="The webhook",
)
def get_webhook(
    request: Request
):
    """
    Get Webhook
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{webhook_id}",
    summary="Update an webhook",
    description="Update an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=None,
    response_description="The updated webhook",
)
def update_webhook(
    request: Request
):
    """
    Update Webhook
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{webhook_id}",
    summary="Delete an webhook",
    description="Delete an webhook",
    tags=["Webhooks"],
    status_code=200,
    response_model=None,
    response_description="The deleted webhook",
)
def delete_webhook(
    request: Request
):
    """
    Delete Webhook
    """
    return {"message": "Not implemented"}
