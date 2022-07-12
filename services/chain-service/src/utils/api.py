import os
from typing import Optional
from urllib.parse import urlparse

import boto3
import requests
from aws_lambda_powertools import Logger, Tracer  # type: ignore
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

ENVIRONMENT = os.environ['ENVIRONMENT']
API_VERSION = 'internal'

if ENVIRONMENT == 'prod':
    VERSIFY_API_URL = f'https://api.versifylabs.com/{API_VERSION}'
else:
    VERSIFY_API_URL = f'https://api-dev.versifylabs.com/{API_VERSION}'

logger = Logger()


def call_api(method: str, path: str, body: dict = {}, organization: Optional[str] = None, params: dict = {}):
    url = urlparse(VERSIFY_API_URL)
    region = boto3.session.Session().region_name
    iam_auth = BotoAWSRequestsAuth(
        aws_host=url.netloc,
        aws_region=region,
        aws_service='execute-api'
    )
    headers = {'X-Organization': organization}
    logger.info({
        'url': VERSIFY_API_URL+path,
        'params': params,
        'json': body,
        'auth': iam_auth,
        'headers': headers
    })

    response = requests.request(
        method=method,
        url=VERSIFY_API_URL+path,
        params=params,
        json=body,
        auth=iam_auth,
        headers=headers
    )
    if not response:
        logger.error(response)
        raise RuntimeError

    logger.info({
        "message": "Response received from internal api",
        "body": response.json()
    })
    return response.json()
