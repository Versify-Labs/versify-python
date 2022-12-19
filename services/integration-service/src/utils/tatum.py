import http.client
import json
import os

from aws_lambda_powertools.utilities import parameters


class Tatum:

    def __init__(self):
        secret_name = os.environ['SECRET_NAME']
        secret = json.loads(parameters.get_secret(secret_name))
        self.conn = http.client.HTTPSConnection(secret['TATUM_API_URL'])
        self.headers = {
            'Content-Type': "application/json",
            'x-api-key': secret['TATUM_API_KEY']
        }
        self.versify_matic_wallet_address = secret['TATUM_MATIC_WALLET_ADDRESS']
        self.versify_matic_wallet_sig_id = secret['TATUM_MATIC_WALLET_SIG_ID']
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
            "signatureId": self.versify_matic_wallet_sig_id,
            "publicMint": public_mint,
            "fee": estimate
        }
        return self.__post(url, payload)

    def mint_token(self, contract, token, to, chain='MATIC', quantity=1):
        url = f"/{self.version}/multitoken/mint"
        estimate = self.estimate_gas(chain, type="MINT_NFT")
        estimate = {k: str(v) for k, v in estimate.items()}
        payload = {
            "chain": chain,
            "tokenId": token,
            "to": to,
            "contractAddress": contract,
            "amount": quantity,
            "signatureId": self.versify_matic_wallet_sig_id,
            "fee": estimate
        }
        return self.__post(url, payload)
