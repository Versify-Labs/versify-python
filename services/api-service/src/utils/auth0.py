import http.client
import json
import os

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities import parameters

from auth0.v3.management import Auth0

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

SECRET_NAME = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET_NAME)
AUTH0_DOMAIN = SECRET['AUTH0_DOMAIN']
AUTH0_M2M_CLIENT_ID = SECRET['AUTH0_M2M_CLIENT_ID']
AUTH0_M2M_CLIENT_SECRET = SECRET['AUTH0_M2M_CLIENT_SECRET']
AUTH0_MGMT_API_AUDIENCE = f'https://{AUTH0_DOMAIN}/api/v2/'
AUTH0_MGMT_API_BASE_URL = f"https://{AUTH0_DOMAIN}"


def init_auth0():
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_M2M_CLIENT_ID,
        "client_secret": AUTH0_M2M_CLIENT_SECRET,
        "audience": AUTH0_MGMT_API_AUDIENCE
    }
    headers = {'content-type': "application/json"}
    conn.request(
        method="POST",
        url="/oauth/token",
        body=json.dumps(payload),
        headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    access_token = data.get('access_token')
    auth0 = Auth0(AUTH0_DOMAIN, access_token)
    return auth0
