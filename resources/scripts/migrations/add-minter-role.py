import http.client
import json
import os

from aws_lambda_powertools.utilities import parameters

SECRET_NAME = os.environ['SECRET_NAME']
SECRET = json.loads(parameters.get_secret(SECRET_NAME))
TATUM_API_KEY = SECRET['TATUM_API_KEY']
TATUM_API_URL = SECRET['TATUM_API_URL']
VERSIFY_MATIC_WALLET_ADDRESS = SECRET['TATUM_MATIC_WALLET_ADDRESS']
VERSIFY_MATIC_WALLET_SIG_ID = SECRET['TATUM_MATIC_WALLET_SIG_ID']


class Tatum:

    def __init__(self):
        api_key = TATUM_API_KEY
        api_url = TATUM_API_URL
        self.conn = http.client.HTTPSConnection(api_url)
        self.headers = {
            'Content-Type': "application/json",
            'x-api-key': api_key
        }
        self.versify_matic_wallet_address = VERSIFY_MATIC_WALLET_ADDRESS
        self.versify_matic_wallet_sig_id = VERSIFY_MATIC_WALLET_SIG_ID
        self.version = 'v3'

    def __post(self, url, payload):
        headers = self.headers
        body = json.dumps(payload)
        self.conn.request("POST", url, headers=headers, body=body)
        res = self.conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))

    def add_minter(self, contract_address, chain='MATIC'):
        url = f"/{self.version}/multitoken/mint/add"
        estimate = self.estimate_gas(chain, type="DEPLOY_NFT")
        estimate = {k: str(v) for k, v in estimate.items()}
        payload = {
            "chain": chain,
            "contractAddress": contract_address,
            "minter": self.versify_matic_wallet_address,
            "signatureId": self.versify_matic_wallet_sig_id,
            "fee": estimate
        }
        return self.__post(url, payload)

    def estimate_gas(self, chain: str, type: str):
        url = f"/{self.version}/blockchain/estimate"
        payload = {
            "chain": chain,
            "type": type
        }
        return self.__post(url, payload)


if __name__ == '__main__':
    tatum = Tatum()

    # Get all collections

    # For each collection, add Versify minter role
