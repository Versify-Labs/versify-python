import json
import os
import warnings
from typing import Any, Dict, Optional, Set

import requests
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities import parameters

__version__ = "5.7.0"
logger = Logger()

SECRET_RAW = parameters.get_secret(os.environ["SECRET_NAME"])
SECRET = json.loads(SECRET_RAW)
STYTCH_ENV = "live" if os.environ["ENVIRONMENT"] == "prod" else "test"
STYTCH_SECRET = SECRET["STYTCH_SECRET"]
STYTCH_PROJECT_ID = SECRET["STYTCH_PROJECT_ID"]
STYTCH_PUBLIC_TOKEN = SECRET["STYTCH_PUBLIC_TOKEN"]


def _env_url(env: str, suppress_warnings: bool = False) -> str:
    """Resolve the base URL for the Stytch API environment."""

    # Supported production environments
    if env == "test":
        if not suppress_warnings:
            warnings.warn("Test version of Stytch not intended for production use")
        return "https://test.stytch.com/v1/"
    elif env == "live":
        return "https://api.stytch.com/v1/"

    # Internal development override. URL builders assume the base URL has a
    # trailing slash, so add one if it's missing.
    if not env.endswith("/"):
        return env + "/"
    return env


class Stytch:
    def __init__(self, project_id, secret, environment="test"):
        self._requester_base = requests
        self.base_url = _env_url(environment, True)
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Stytch Python v{}".format(__version__),
        }
        self.auth = requests.auth.HTTPBasicAuth(project_id, secret)

    @property
    def user_url(self):
        return self.get_url("users")

    def get_url(self, arg: str):
        return "{0}{1}".format(self.base_url, arg)

    def _validate_options(self, options: Dict[str, bool]) -> Dict[str, bool]:
        if not options:
            return options

        default_options = {}
        if options.get("ip_match_required"):
            default_options.update({"ip_match_required": options["ip_match_required"]})
        if options.get("user_agent_match_required"):
            default_options.update(
                {"user_agent_match_required": options["user_agent_match_required"]}
            )

        return default_options

    def _validate_attributes(self, attributes: Dict[str, str]) -> bool:
        if not attributes:
            return True
        return self._validate_fields(
            set(["ip_address", "user_agent"]), set(attributes.keys())
        )

    def _validate_fields(self, accepted_fields: Set[str], fields: Set[str]) -> bool:
        if len(accepted_fields.union(fields)) > len(accepted_fields):
            raise Exception("Unknown arguments applied")

        return True

    def _get(self, url: str, query_params: Dict = {}):
        response = self._requester_base.get(
            url, auth=self.auth, headers=self.headers, params=query_params
        )
        return response.json()

    def _post(self, url: str, data: Dict):
        response = self._requester_base.post(
            url, auth=self.auth, headers=self.headers, data=json.dumps(data)
        )
        return response.json()

    def _put(self, url: str, data: Dict):
        response = self._requester_base.put(
            url, auth=self.auth, headers=self.headers, data=json.dumps(data)
        )
        return response.json()

    def _delete(self, url: str):
        response = self._requester_base.delete(
            url, auth=self.auth, headers=self.headers
        )
        return response.json()

    def create_user(
        self,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        create_user_as_pending: Optional[bool] = False,
        attributes: Optional[Dict[str, str]] = None,
    ):
        data: Dict[str, Any] = {
            "email": email,
            "phone_number": phone_number,
            "name": {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
            },
            "create_user_as_pending": create_user_as_pending,
        }
        if attributes and self._validate_attributes(attributes):
            data.update({"attributes": attributes})
        return self._post("{0}".format(self.user_url), data)

    def get_user(self, user_id: str):
        return self._get("{0}/{1}".format(self.user_url, user_id))


def stytch():
    return Stytch(
        project_id=STYTCH_PROJECT_ID, secret=STYTCH_SECRET, environment=STYTCH_ENV
    )
