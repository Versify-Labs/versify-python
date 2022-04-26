import random
import string

from pynamodb.exceptions import DoesNotExist
from versify.utilities.model import generate_uuid

from .model import Account, Profile


class WalletService:

    def __init__(self, email):
        self.email = email

    def create_account(self, issuer, address=None, chain=None, description=''):
        payload = {
            'PK': self.email,
            'SK': issuer,
            'address': address,
            'chain': chain,
            'description': description,
            'email': self.email,
            'id': issuer,
        }
        account = Account(**payload)
        account.save()
        return account

    def create_profile(self, phone=None):
        seed = ''.join(random.choice(string.ascii_letters) for i in range(10))
        payload = {
            'PK': self.email,
            'SK': self.email,
            'avatar': f'https://avatars.dicebear.com/api/avataaars/{seed}.svg',
            'email': self.email,
            'handle': self.email.split('@')[0],
            'name': self.email.split('@')[0],
            'phone': phone
        }
        profile = Profile(**payload)
        profile.save()
        return profile

    def get_account(self, id):
        try:
            return Account.get(self.email, id)
        except DoesNotExist:
            return None

    def get_profile(self):
        try:
            return Profile.get(self.email, self.email)
        except DoesNotExist:
            return None

    def list_accounts(self):
        accounts = Account.object_index.query(
            hash_key=self.email,
            range_key_condition=Account.object == 'account'
        )
        return accounts

    def sync_authorizer(self, authorizer):
        issuer = authorizer.get('issuer')
        phone = authorizer.get('phone')
        _, chain, address = issuer.split(':')

        # Get profile / create if it doesnt exist
        profile = self.get_profile()
        if not profile:
            profile = self.create_profile(phone)

        # Get account / create if it doesnt exist
        account = self.get_account(issuer)
        if not account:
            account = self.create_account(issuer, address, chain)

        # TODO: Mint any unminted assets?
