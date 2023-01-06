import logging
import secrets
import time

from bson.objectid import ObjectId
from eth_account import Account
from jose import jwt
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import UserConfig
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.images import get_image
from ..utils.mongo import mdb
from ..utils.stytch import stytch


class UserService(ExpandableResource):
    def __init__(self, account_service) -> None:
        self.collection = mdb[UserConfig.db][UserConfig.collection]
        self.expandables = UserConfig.expandables
        self.Model = UserConfig.model
        self.object = UserConfig.object
        self.prefix = UserConfig.prefix
        self.search_index = UserConfig.search_index

        # Wallet collection
        self.wallet_collection = mdb["Accounts"]["Wallets"]

        # Internal services
        self.account_service = account_service

    def get(self, email: str, body: dict = {}) -> dict:
        body["email"] = email

        # Check if user exists
        stytch_user = body.get("stytch_user")
        user_id = body.get("id")
        user_filter = self.get_user_filter(user_id, email, stytch_user)
        user = self.collection.find_one(user_filter)

        # If user exists, update with any new data
        if user:

            # See if we need to update the user
            needs_update = False
            user = self.Model(**user).to_json()
            for k, v in body.items():
                if user.get(k) != v:
                    needs_update = True
            if needs_update:
                user = deep_update(user, body)
                user["updated"] = int(time.time())
                validated_user = self.Model(**user)
                updated_user = self.collection.find_one_and_update(
                    filter={"_id": user_id},
                    update={"$set": validated_user.to_bson()},
                    upsert=True,
                    return_document=ReturnDocument.AFTER,
                )
                user = self.Model(**updated_user).to_json()

        # If user does not exist, create user
        else:

            # Create user
            body["_id"] = body.get("_id", f"{self.prefix}_{ObjectId()}")
            body["created"] = int(time.time())
            body["updated"] = int(time.time())
            body["avatar"] = body.get("avatar", get_image(body.get("name")))
            body["wallets"] = [self.generate_managed_wallet()]
            user = self.Model(**body)
            self.collection.insert_one(user.to_bson())
            user = user.to_json()

        # Expand user accounts before returning
        user["accounts"] = self.list_accounts(email)
        return user

    def get_user_filter(self, user_id, email, stytch_user):
        expressions = []
        if user_id:
            expressions.append({"_id": user_id})
        if email:
            expressions.append({"email": email})
        if stytch_user:
            expressions.append({"stytch_user": stytch_user})
        if not expressions:
            return {}
        return {"$or": expressions}

    def generate_managed_wallet(self):

        # Create address and private key
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        account = Account.privateKeyToAccount(private_key)
        public_address = account.address

        # TODO: Store private key in secrets manager like ADDRESS:PRIVATE_KEY
        self.wallet_collection.insert_one(
            {"address": public_address, "private_key": private_key}
        )

        return {"address": public_address, "managed": True, "type": "ethereum"}

    def list_accounts(self, email):
        accounts = self.account_service.list_by_member_email(email)
        return accounts

    def attach_wallet(self, email: str, address: str, type: str = "ethereum") -> dict:
        """Attach a wallet to the user.

        Args:
            address (str): The address of the wallet to attach.
            type (str): The type of the wallet to attach.

        Returns:
            dict: The user.
        """

        # Find document matching filter
        user = self.get(email)
        old_wallets = user.get("wallets", [])
        for wallet in old_wallets:
            old_address = wallet.get("address", "").lower()
            new_address = address.lower()
            if old_address == new_address:
                return user

        # Create new wallet to attach
        new_wallet = {"address": address, "managed": False, "type": type}
        user = self.collection.find_one_and_update(
            filter={"email": email},
            update={"$push": {"wallets": new_wallet}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return user

    def get_user_by_token(self, token: str):
        """Get a user by token.

        Args:
            token (str): The token to retrieve.

        Returns:
            dict: The user.
        """
        if not token:
            return

        try:
            claims = jwt.get_unverified_claims(token)
        except jwt.JWTError:  # type: ignore
            return
        if not claims:
            return

        # Verify the claims are valid
        session = claims.get("https://stytch.com/session")
        stytch_user_id = claims.get("sub")
        if not session or not stytch_user_id:
            return

        # Build user object
        auth_factors = session.get("authentication_factors", [])
        email = None
        body = {"stytch_user": stytch_user_id}
        for factor in auth_factors:

            # Handle OAuth session
            if factor.get("type") == "oauth":
                user = stytch().get_user(stytch_user_id)
                email = user["emails"][0]["email"]
                body["first_name"] = user["name"].get("first_name")
                body["last_name"] = user["name"].get("last_name")

                # NOTE: We cannot use this because the URL changes
                # if user['providers'] and len(user['providers']) > 0:
                #     provider = user['providers'][0]
                #     body['avatar'] = provider.get('profile_picture_url')

            # Handle magic link or OTP session
            if factor.get("type") in ["magic_link", "otp"]:
                email_factor = factor.get("email_factor", {})
                email = email_factor.get("email_address")

        return self.get(email, body) if email else None

    def retrieve_by_id(self, user_id: str) -> dict:
        """Get an user by id.

        Args:
            user_id (str): The id of the user to retrieve.

        Returns:
            dict: The user.
        """
        logging.info("Retrieving user", extra={"id": user_id})

        # Find document matching filter
        user = self.collection.find_one(filter={"_id": user_id})
        if not user:
            raise NotFoundError

        # Convert to JSON
        user = self.Model(**user).to_json()

        return user
