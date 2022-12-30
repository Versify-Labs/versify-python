import json
import logging
import os
import pathlib
from typing import List, Union

from aws_lambda_powertools.utilities import parameters
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


def get_parameter(parameter_name):
    return parameters.get_parameter(parameter_name)


def get_secret_parameter(parameter_name):
    secret_name = '/versify/platform/secret'
    secret = parameters.get_secret(secret_name)
    secret = json.loads(secret) if secret else {}  # type: ignore
    return secret.get(parameter_name)


def get_var(name, default=None):
    if name in os.environ:
        return os.environ[name]
    # elif get_parameter(name):
    #     return get_parameter(name)
    # elif get_secret_parameter(name):
    #     return get_secret_parameter(name)
    elif default:
        return default
    else:
        logging.warning(f'Could not find {name} in environment or secrets')
        return 'false'


class Settings(BaseSettings):

    class Config:
        case_sensitive = True

    # FastAPI Settings
    API_V1_STR: str = "/api/v1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Custom Variables
    AWS_ENABLED = get_var('AWS_LAMBDA_FUNCTION_NAME')
    AWS_ACCOUNT_ID = get_var('AWS_ACCOUNT', '424532774130')
    AWS_REGION = get_var('AWS_REGION', 'us-east-1')
    MANDRILL_API_KEY = get_var('MANDRILL_API_KEY')
    MONGO_DOMAIN = get_var('MONGO_DOMAIN')
    MONGO_UN = get_var('MONGO_UN')
    MONGO_PW = get_var('MONGO_PW')
    MONGO_DB_URL = get_var('MONGO_DB_URL')
    PARAGON_SECRET_KEY = get_var('PARAGON_SECRET_KEY')
    PARAGON_SIGNING_KEY = get_var('PARAGON_SIGNING_KEY')
    SLACK_CHANNEL = get_var('SLACK_CHANNEL_ID')
    SLACK_TOKEN = get_var('SLACK_API_TOKEN')
    STEP_FUNCTION_LAMBDA_ARN = f'arn:aws:lambda:{AWS_REGION}:{AWS_ACCOUNT_ID}:function:AutomationService-RunTask'
    STEP_FUNCTION_LOG_ARN = get_var('STEP_FUNCTION_LOG_ARN')
    STEP_FUNCTION_ROLE_ARN = get_var('STEP_FUNCTION_ROLE_ARN')
    STEP_FUNCTION_ARN_BASE = f'arn:aws:states:{AWS_REGION}:{AWS_ACCOUNT_ID}:stateMachine:'
    STRIPE_SECRET_KEY = get_var('STRIPE_SECRET_KEY')
    STRIPE_PUBLIC_KEY = get_var('STRIPE_PUBLIC_KEY')
    STRIPE_WEBHOOK_SECRET = get_var('STRIPE_WEBHOOK_SECRET')
    STRIPE_GROWTH_PRICE = get_var('STRIPE_GROWTH_PRICE')
    STYTCH_ENV = get_var('STYTCH_ENV', 'test')
    STYTCH_PROJECT_ID = get_var('STYTCH_PROJECT_ID')
    STYTCH_PUBLIC_TOKEN = get_var('STYTCH_PUBLIC_TOKEN')
    STYTCH_SECRET = get_var('STYTCH_SECRET')
    TATUM_API_KEY = get_var('TATUM_API_KEY')
    TATUM_API_URL = get_var('TATUM_API_URL')
    TATUM_MATIC_WALLET_ADDRESS = get_var('TATUM_MATIC_WALLET_ADDRESS')
    TATUM_MATIC_WALLET_SIG_ID = get_var('TATUM_MATIC_WALLET_SIG_ID')

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
