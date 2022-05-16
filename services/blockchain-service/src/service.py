import http.client
import json
import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities import parameters
from pynamodb.exceptions import DoesNotExist

from .model import SignatureModel, TransactionModel

SECRET_NAME = os.environ['SECRET_NAME']
SECRET = json.loads(parameters.get_secret(SECRET_NAME))
TATUM_API_KEY = SECRET['TATUM_API_KEY']
TATUM_API_URL = SECRET['TATUM_API_URL']
VERSIFY_MATIC_SIG_ID = SECRET['TATUM_MATIC_SIG_ID']

logger = Logger()


class Tatum:

    def __init__(self):
        api_key = TATUM_API_KEY
        api_url = TATUM_API_URL
        self.conn = http.client.HTTPSConnection(api_url)
        self.headers = {
            'Content-Type': "application/json",
            'x-api-key': api_key
        }
        self.versify_matic_sig_id = VERSIFY_MATIC_SIG_ID
        self.version = 'v3'

    def __get(self, url):
        headers = self.headers
        self.conn.request("GET", url, headers=headers)
        res = self.conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))

    def __post(self, url, payload):
        headers = self.headers
        body = json.dumps(payload)
        self.conn.request("POST", url, headers=headers, body=body)
        res = self.conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))

    def estimate_gas(self, chain: str, type: str):
        url = f"/{self.version}/blockchain/estimate"
        payload = {
            "chain": chain,
            "type": type
        }
        return self.__post(url, payload)

    def get_transaction(self, hash):
        url = f"/{self.version}/polygon/transaction/{hash}"
        return self.__get(url)

    def get_transaction_details(self, id):
        url = f"/{self.version}/kms/{id}"
        return self.__get(url)

    def deploy_contract(self, uri, chain='MATIC', public_mint=False):
        """Create a new contract"""
        url = f"/{self.version}/multitoken/deploy"
        estimate = self.estimate_gas(chain, type="DEPLOY_NFT")
        estimate = {k: str(v) for k, v in estimate.items()}
        payload = {
            "chain": chain,
            "uri": uri,
            "signatureId": self.versify_matic_sig_id,
            "publicMint": public_mint,
            "fee": estimate
        }
        logger.info(payload)
        return self.__post(url, payload)

    def mint_token(self, contract, token, to, chain='MATIC', quantity=1):
        url = f"/{self.version}/multitoken/mint"
        payload = {
            "chain": chain,
            "tokenId": token,
            "to": to,
            "contractAddress": contract,
            "amount": quantity,
            "signatureId": self.versify_matic_sig_id,
        }
        return self.__post(url, payload)


class Signatures:

    def __init__(self):
        self.model = SignatureModel

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, id: str, body: dict = {}, raw: bool = True):
        """Create a new signature"""
        body['PK'] = id
        body['SK'] = id
        body['id'] = id
        signature = self.model(**body)
        signature.save()
        return signature.to_dict() if raw else signature

    def get(self, id: str, raw: bool = True):
        """Retrieves an signature by its id"""
        try:
            item = self.model.get(id, id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing signature"""
        signature = self.get(id, raw=False)
        actions = []
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        signature.update(actions=actions)
        return signature.to_dict() if raw else signature

    def list_by_status(self, status: str, query: dict = {}, raw: bool = True):
        """List signatures by status"""
        signatures = self.model.by_object_by_status.query(
            hash_key='signature',
            range_key_condition=self.model.status == status
        )
        return self.to_list(signatures) if raw else signatures


class Transactions:

    def __init__(self):
        self.model = TransactionModel

    def convert_tatum_txn(self, tatum_txn: dict):
        """Convert tatum transaction to internal"""
        tatum_map = {
            'blockHash': 'block_hash',
            'blockNumber': 'block_num',
            'contractAddress': 'contract_address',
            'from': 'from_address',
            'status': 'success',
            'to': 'to_address',
            'transactionHash': 'id'
        }
        body = {'status': 'complete'}
        for k, v in tatum_txn.items():
            if k in tatum_map:
                body[tatum_map[k]] = v
        return body

    def create(self, id: str, body: dict = {}, raw: bool = True):
        """Create a new transaction"""
        body['PK'] = id
        body['SK'] = id
        body['id'] = id
        transaction = self.model(**body)
        transaction.save()
        return transaction.to_dict() if raw else transaction


class Versify:

    def __init__(self) -> None:
        self.signatures = Signatures()
        self.transactions = Transactions()
