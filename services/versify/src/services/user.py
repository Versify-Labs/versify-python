import secrets
import time

from aws_lambda_powertools import Logger, Tracer
from bson.objectid import ObjectId
from eth_account import Account
from pymongo.collection import ReturnDocument

from ..api.errors import NotFoundError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb

logger = Logger()
tracer = Tracer()


class UserService(ExpandableResource):

    def __init__(self, account_service) -> None:
        _config = config['user']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

        # Internal services
        self.account_service = account_service

    def get_user_filter(self, user_id, email, stytch_user):
        expressions = []
        if user_id:
            expressions.append({'_id': user_id})
        if email:
            expressions.append({'email': email})
        if stytch_user:
            expressions.append({'stytch_user': stytch_user})
        if not expressions:
            return {}
        return {'$or': expressions}

    def list_accounts(self, email):
        logger.info('Listing user accounts', extra={'email': email})
        accounts = self.account_service.list_by_member_email(email)
        return accounts

    def retrieve_by_email(self, email: str) -> dict:
        """Get an user by email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            dict: The user.

        Raises:
            NotFoundError: If the user does not exist.
        """
        logger.info('Retrieving user by email', extra={'email': email})

        # Find document matching filter
        user = self.collection.find_one(filter={'email': email})
        if not user:
            raise NotFoundError

        # Convert to JSON
        user = self.Model(**user).to_json()

        return user

    def retrieve_by_id(self, user_id: str) -> dict:
        """Get a user by id.

        Args:
            user_id (str): The id of the user to retrieve.

        Returns:
            dict: The user.

        Raises:
            NotFoundError: If the user does not exist.
        """
        logger.info('Retrieving user by id', extra={'user_id': user_id})

        # Find document matching filter
        user = self.collection.find_one(filter={'_id': user_id})
        if not user:
            raise NotFoundError

        # Convert to JSON
        user = self.Model(**user).to_json()

        # Expand user accounts
        user['accounts'] = self.list_accounts(email=user['email'])

        return user

    def create(self, body: dict) -> dict:
        """Create a new user. If the user already exists, update the user.

        Args:
            user (dict): The user to create.

        Returns:
            dict: The user.
        """
        logger.info('Creating user', extra={'user': body})

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Create managed wallet
        managed_wallet = self.generate_managed_wallet()
        wallets = body.get('wallets', [])
        wallets.append(managed_wallet)
        body['wallets'] = wallets

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def update(self, user_id: str, update: dict):
        """Update a user. If the user does not exist, create a new user.

        Args:
            user_id (str): The id of the user to update.
            update (dict): The fields to update.

        Returns:
            dict: The user.

        Raises:
            NotFoundError: If the user does not exist.
        """
        logger.info('Updating user', extra={'user': update})

        # Find document matching filter
        user = self.collection.find_one(filter={'_id': user_id})
        if not user:
            raise NotFoundError

        # Update fields
        user = {**user, **update}
        user['updated'] = int(time.time())

        # Validate against schema
        validated_user = self.Model(**user)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': user_id},
            update={'$set': validated_user.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, user_id: str) -> bool:
        """Delete an user.

        Args:
            user_id (str): The id of the user to delete.

        Returns:
            bool: True if the user was deleted, False otherwise.
        """

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': user_id
        })
        if not deleted:
            raise NotFoundError

        return True

    def sync(self, user_body: dict) -> dict:
        """Sync a user with new data from auth provider.

        Args:
            user_body (dict): The data to sync with the existing/new user.

        Returns:
            dict: The user after the sync.
        """
        logger.info('User sync', extra={'user_body': user_body})

        # Parse user body
        user_id = user_body.get('id')
        email = user_body.get('email')
        stytch_user = user_body.get('stytch_user')

        # Check if user exists
        user_filter = self.get_user_filter(user_id, email, stytch_user)
        user = self.collection.find_one(user_filter)

        # If user exists, update with any new data
        if user:

            # Convert to JSON
            user = self.Model(**user).to_json()

            needs_update = False
            for k, v in user_body.items():
                if user.get(k) != v:
                    needs_update = True
            if needs_update:
                user = self.update(user['id'], user_body)

        # If user does not exist, create user
        else:
            user = self.create(user_body)

        # Expand user accounts
        data = self.retrieve_by_email(user['email'])
        data['accounts'] = self.list_accounts(email=email)

        return data

    def generate_managed_wallet(self):

        # Create address and private key
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        account = Account.privateKeyToAccount(private_key)
        public_address = account.address

        # TODO: Store private key in secrets manager like ADDRESS:PRIVATE_KEY

        return {
            'address': public_address,
            'managed': True,
            'private_key': private_key,
            'type': 'ethereum'
        }
