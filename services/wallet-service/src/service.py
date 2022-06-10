import time

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from pynamodb.exceptions import DoesNotExist

from .model import AccountModel

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


class Accounts:

    def __init__(self, email: str):
        self.model = AccountModel
        self.wallet = f'wallet_{email}'

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new account"""
        account_id = f'account_{body["issuer"]}'
        timestamp = int(time.time())
        body['PK'] = f'{self.wallet}:account'
        body['id'] = account_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['wallet'] = self.wallet
        account = self.model(**body)
        account.save()
        return account.to_dict() if raw else account

    def list(self, raw: bool = True):
        """Retrieves a list of accounts by a wallet"""
        accounts = self.model.by_wallet.query(
            hash_key=f'{self.wallet}:account'
        )
        return self.to_list(accounts) if raw else accounts

    def get(self, account_id: str, raw: bool = True):
        """Retrieve a account by its id"""
        try:
            item = self.model.get(f'{self.wallet}:account', account_id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, account_id: str, body: dict = {}, raw: bool = True):
        """Update an existing account"""
        account = self.get(account_id, raw=False)
        actions = [self.model.date_updated.set(int(time.time()))]
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        account.update(actions=actions)
        return account.to_dict() if raw else account

    def delete(self, account_id: str):
        """Delete an account"""
        account = self.get(self.wallet, account_id, raw=False)
        account.delete()
        return id


class Versify:

    def __init__(self, email: str) -> None:
        self.accounts = Accounts(email)

    # def sync_authorizer(self, authorizer):
    #     email = authorizer.get('email')
    #     issuer = authorizer.get('issuer')
    #     phone = authorizer.get('phone')
    #     _, chain, address = issuer.split(':')

    #     wallet_id = f'wallet_{email}'

    #     # Get wallet / create if it doesnt exist
    #     wallet = self.wallets.get(wallet_id)
    #     if not wallet:
    #         body = {'email': email, 'phone': 'phone'}
    #         wallet = self.wallets.create(body)

    #     # Get account / create if it doesnt exist
    #     account = self.get_account(issuer)
    #     if not account:
    #         account = self.create_account(
    #             issuer, address, chain)
