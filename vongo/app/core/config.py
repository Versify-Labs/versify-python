import json
import logging
import os
import pathlib
from typing import List, Union

from aws_lambda_powertools.utilities import parameters
from pydantic import AnyHttpUrl, BaseSettings, validator

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent

# Get Secrets from AWS Parameter Store
SECRET = {}
try:
    SECRET = parameters.get_secret("/versify/platform/secret")
    SECRET = json.loads(SECRET) if SECRET else {}  # type: ignore
except:
    pass


def get_var(name, default=None) -> Union[str, None]:
    if name in os.environ:
        return os.environ[name]
    elif name in SECRET:
        return SECRET[name]  # type: ignore
    elif default:
        return default
    else:
        logging.warning(f"Could not find {name} in environment or secrets")
        return None


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    # FastAPI Settings
    API_V1_STR: str = "/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # AWS Lambda Variables
    AWS_ACCOUNT: str = os.environ.get("AWS_ACCOUNT", "424532774130")
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")

    # AWS Secrets Manager
    MONGO_DOMAIN: Union[str, None] = get_var("MONGO_DOMAIN")
    MONGO_UN: Union[str, None] = get_var("MONGO_UN")
    MONGO_PW: Union[str, None] = get_var("MONGO_PW")
    MONGO_DB_URL: Union[str, None] = get_var("MONGO_DB_URL")
    STYTCH_ENV: Union[str, None] = get_var("STYTCH_ENV", "test")
    STYTCH_PROJECT_ID: Union[str, None] = get_var("STYTCH_PROJECT_ID")
    STYTCH_SECRET: Union[str, None] = get_var("STYTCH_SECRET")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
