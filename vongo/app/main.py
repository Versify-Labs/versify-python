from pathlib import Path

from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import APIRouter, FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

__version__ = "0.1.0"

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
)

root_router = APIRouter()


@root_router.get(path="/", tags=["Root"], status_code=200)
def root(request: Request):
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        name="index.html",
        context={"request": request, "recipes": []},
    )


app.include_router(root_router, include_in_schema=False)
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
