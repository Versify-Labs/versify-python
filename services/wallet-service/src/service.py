import random
import string

from pynamodb.exceptions import DoesNotExist

from .model import BlockchainAddress, Wallet


class WalletService:

    def __init__(self, email):
        self.email = email

    def create_wallet(self, phone=None):
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
        wallet = Wallet(**payload)
        wallet.save()
        return wallet

    def get_wallet(self):
        try:
            return Wallet.get(self.email, self.email)
        except DoesNotExist:
            return None

    def create_blockchain_address(self, issuer, address=None, chain=None, description=''):
        payload = {
            'PK': self.email,
            'SK': issuer,
            'address': address,
            'chain': chain,
            'description': description,
            'email': self.email,
            'id': issuer,
        }
        blockchain_address = BlockchainAddress(**payload)
        blockchain_address.save()
        return blockchain_address

    def get_blockchain_address(self, id):
        try:
            return BlockchainAddress.get(self.email, id)
        except DoesNotExist:
            return None

    def list_blockchain_addresses(self):
        blockchain_addresses = BlockchainAddress.by_email_by_object.query(
            hash_key=self.email,
            range_key_condition=BlockchainAddress.object == 'blockchain_address'
        )
        return blockchain_addresses

    def update_blockchain_address(self, id, description):
        blockchain_address = self.get_blockchain_address(id)
        blockchain_address.update(
            actions=[BlockchainAddress.description.set(description)])
        return blockchain_address

    def sync_authorizer(self, authorizer):
        issuer = authorizer.get('issuer')
        phone = authorizer.get('phone')
        _, chain, address = issuer.split(':')

        # Get wallet / create if it doesnt exist
        wallet = self.get_wallet()
        if not wallet:
            wallet = self.create_wallet(phone)

        # Get blockchain_address / create if it doesnt exist
        blockchain_address = self.get_blockchain_address(issuer)
        if not blockchain_address:
            blockchain_address = self.create_blockchain_address(
                issuer, address, chain)

        # TODO: Mint any unminted assets?
