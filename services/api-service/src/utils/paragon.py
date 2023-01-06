import json
import os
import time

from aws_lambda_powertools.utilities import parameters
from jose import jwt


class Paragon:
    def __init__(self):
        pass

    def generate_token(self, account_id: str):
        """Generate a Paragon token for an account.

        Args:
            account_id (str): The id of the account to get a Paragon token for.

        Returns:
            dict: The Paragon token.
        """
        secret_name = os.environ["SECRET_NAME"]
        secret_raw = parameters.get_secret(secret_name)
        secret = json.loads(secret_raw)  # type: ignore
        signing_key = secret["PARAGON_SIGNING_KEY"]
        created = int(time.time())
        token = jwt.encode(
            {
                "sub": account_id,
                "iat": created,
                "exp": created + 60 * 60,
            },
            signing_key,
            algorithm="RS256",
        )
        return token
