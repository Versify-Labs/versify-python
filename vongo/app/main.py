from pathlib import Path

from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import APIRouter, FastAPI, Request
from fastapi.templating import Jinja2Templates
from mangum import Mangum

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

__version__ = "1.0.0"

app = FastAPI(
    title="Versify API",
    description="Versify API documentation",
    contact={
        "name": "Versify Labs",
        "url": "https://versifylabs.com",
        "email": "support@versifylabs.com",
    },
    terms_of_service="https://versifylabs.com/legal/terms",
    version=__version__,
    openapi_tags=[
        {
            "name": "Accounts",
            "description": "Operations related to creating, reading, updating and deleting accounts.",
        },
        {
            "name": "Assets",
            "description": "Operations related to creating, reading, updating and deleting assets.",
        },
        {
            "name": "Claims",
            "description": "Operations related to creating, reading, updating and deleting claims.",
        },
        {
            "name": "Collections",
            "description": "Operations related to creating, reading, updating and deleting collections.",
        },
        {
            "name": "Contacts",
            "description": "Operations related to creating, reading, updating and deleting contacts.",
        },
        {
            "name": "Events",
            "description": "Operations related to creating, reading, updating and deleting events.",
        },
        {
            "name": "Journeys",
            "description": "Operations related to creating, reading, updating and deleting journeys.",
        },
        {
            "name": "Messages",
            "description": "Operations related to creating, reading, updating and deleting messages.",
        },
        {
            "name": "Mints",
            "description": "Operations related to creating, reading, updating and deleting mints.",
        },
        {
            "name": "Redemptions",
            "description": "Operations related to creating, reading, updating and deleting redemptions.",
        },
        {
            "name": "Rewards",
            "description": "Operations related to creating, reading, updating and deleting rewards.",
        },
        {
            "name": "Webhooks",
            "description": "Operations related to creating, reading, updating and deleting webhooks.",
        },
        {
            "name": "Users",
            "description": "Operations related to creating, reading, updating and deleting users.",
        },
    ],
)


root_router = APIRouter()


@root_router.get(path="/", tags=["Root"], status_code=200)
def root(request: Request):
    return TEMPLATES.TemplateResponse(
        name="index.html",
        context={"request": request, "recipes": []},
    )


@root_router.get(path="/info", tags=["Root"], status_code=200)
def info():
    return settings.dict()


app.include_router(root_router, include_in_schema=False)
app.include_router(api_router, prefix=settings.API_V1_STR)

handler = Mangum(app)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
