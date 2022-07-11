import os
from typing import Tuple
from urllib.parse import urlparse

import boto3
import requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

ENVIRONMENT = os.environ['ENVIRONMENT']
if ENVIRONMENT == 'prod':
    VERSIFY_API_URL = 'https://api.versifylabs.com'
else:
    VERSIFY_API_URL = 'https://api-dev.versifylabs.com'


def call_api(method: str, path: str, body: dict = {}, organization: str = None, params: dict = {}):
    url = urlparse(VERSIFY_API_URL)
    region = boto3.session.Session().region_name
    iam_auth = BotoAWSRequestsAuth(
        aws_host=url.netloc,
        aws_region=region,
        aws_service='execute-api'
    )
    headers = {'X-Organization': organization}
    print({
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
    print({
        "message": "Response received from internal api",
        "body": response.json()
    })
    return response.json()


def call_external_api(method: str, url: str, organization: str, body: dict = {}, params: dict = {}):
    headers = {
        'Versify-Signature': 'Not Implemented',
        'X-Organization': organization,
    }
    print({
        'method': method,
        'headers': headers,
        'json': body,
        'params': params,
        'url': url,
    })

    response = requests.request(
        headers=headers,
        json=body,
        method=method,
        params=params,
        url=url
    )
    return response
