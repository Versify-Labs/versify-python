from pathlib import Path

from aws_lambda_powertools import Logger, Metrics, Tracer
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from mangum import Mangum

from .api.api_v1.api import api_router
from .core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

logger: Logger = Logger()
metrics: Metrics = Metrics()
tracer: Tracer = Tracer()

app = FastAPI(
    title=settings.API_NAME,
    description="Versify API documentation",
    contact={
        "name": "Versify Labs",
        "url": "https://versifylabs.com",
        "email": "support@versifylabs.com",
    },
    servers=[
        # {
        #     "url": "https://api.versifylabs.com",
        #     "description": "Production server",
        # },
        {
            "url": "https://api-dev.versifylabs.com",
            "description": "Development server",
        },
        {
            "url": "http://127.0.0.1:8000",
            "description": "Local server",
        },
    ],
    terms_of_service="https://versifylabs.com/legal/terms",
    version=settings.API_VERSION,
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
            "name": "Notes",
            "description": "Operations related to creating, reading, updating and deleting notes.",
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
            "name": "Tags",
            "description": "Operations related to creating, reading, updating and deleting tags.",
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_router = APIRouter()


@root_router.get(path="/", tags=["Root"], status_code=200, include_in_schema=False)
def root(request: Request):
    return TEMPLATES.TemplateResponse(
        name="index.html",
        context={"request": request, "recipes": []},
    )


@root_router.get(path="/info", tags=["Root"], status_code=200, include_in_schema=False)
def info():
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
    }


app.include_router(root_router, include_in_schema=True)
app.include_router(api_router, prefix=settings.API_V1_STR)


handler = Mangum(app)
handler = logger.inject_lambda_context(handler, clear_state=True)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
