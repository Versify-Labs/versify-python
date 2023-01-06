import time

from jose import jwt

from ..config import ParagonConfig


class Paragon:
    def __init__(self):
        self.secret_key = ParagonConfig.PARAGON_SECRET_KEY
        self.signing_key = ParagonConfig.PARAGON_SIGNING_KEY

    def generate_token(self, account_id: str):
        """Generate a Paragon token for an account.

        Args:
            account_id (str): The id of the account to get a Paragon token for.

        Returns:
            dict: The Paragon token.
        """
        created = int(time.time())
        token = jwt.encode(
            {
                "sub": account_id,
                "iat": created,
                "exp": created + 60 * 60,
            },
            self.signing_key,
            algorithm="RS256",
        )
        return token
