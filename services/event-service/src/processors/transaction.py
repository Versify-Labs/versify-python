from aws_lambda_powertools import Logger

from ..utils.api import call_api
from ..utils.tatum import Tatum

logger = Logger()
tatum = Tatum()


class TransactionProcessor:

    def __init__(self, txn) -> None:
        self.txn = txn

    def validate(self):
        return True

    def match_collection(self, signature):
        response = call_api(
            method='GET',
            path='/internal/collections',
            params={'signature': signature}
        )
        logger.info(response)

        collections = response.get('data')
        if not collections or len(collections) < 1:
            logger.error('No matching collections for signature ', signature)
            return None

        return collections[0]

    def match_mint(self, signature):
        response = call_api(
            method='GET',
            path='/internal/mints',
            params={'signature': signature}
        )
        logger.info(response)

        mints = response.get('data')
        if not mints or len(mints) < 1:
            logger.error('No matching mints for signature ', signature)
            return None

        return mints[0]

    def update_collection(self, id, body, account):
        response = call_api(
            method='PUT',
            path=f'/internal/collections/{id}',
            body=body,
            account=account
        )
        logger.info(response)
        if not response:
            logger.error('Could not update collection')
            raise RuntimeError

    def update_mint(self, id, body, account):
        response = call_api(
            method='PUT',
            path=f'/internal/mints/{id}',
            body=body,
            account=account
        )
        logger.info(response)
        if not response:
            logger.error('Could not update mint')
            raise RuntimeError

    def start(self):
        self.validate()

        txn = self.txn
        sig_id = txn['signatureId']
        txn_id = txn['txId']
        sub_type = txn['subscriptionType']
        status = 'complete' if sub_type == 'KMS_COMPLETED_TX' else 'failed'
        logger.info({'status': status})

        # Get details from Tatum
        txn_details = tatum.get_transaction_details(sig_id)
        logger.info(txn_details)
        if not txn_details:
            logger.error('Could not get transaction details')
            raise RuntimeError

        # Get txn from tatum
        tatum_txn = tatum.get_transaction(txn_id)
        logger.info(tatum_txn)
        if not tatum_txn:
            logger.error('Could not get transaction')
            raise RuntimeError

        # Get collection with matching signature
        collection = self.match_collection(sig_id)
        if collection:
            collection_id = collection['id']
            account = collection['account']

            # Create update body based on tatum txn
            status = 'deployed' if sub_type == 'KMS_COMPLETED_TX' else 'failed'
            update_body = {
                'contract_address': tatum_txn.get('contractAddress'),
                'status': status,
                'transaction': txn_id
            }

            # Save Updated Collection to DB
            self.update_collection(collection_id, update_body, account)

        # Get mint with matching signature
        mint = self.match_mint(sig_id)
        if mint:
            mint_id = mint['id']
            account = mint['account']

            # Create update body based on tatum txn
            status = 'complete' if sub_type == 'KMS_COMPLETED_TX' else 'failed'
            update_body = {
                'status': status,
                'transaction': txn_id
            }

            # Save Updated Mint to DB
            self.update_mint(mint_id, update_body, account)

        return True
