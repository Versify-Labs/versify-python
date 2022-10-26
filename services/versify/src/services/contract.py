from aws_lambda_powertools import Logger, Tracer

from ..interfaces.expandable import ExpandableResource

logger = Logger()
tracer = Tracer()


class ContractService(ExpandableResource):

    def __init__(self):
        pass

    def deploy(self):
        pass

    def mint_token(self, contract_address, metadata, owner):
        pass

    def transfer_token(self, contract_address, token_id, to_address):
        pass

    def get_token_balance(self, contract_address, token_id, owner_address):
        pass

    def get_token_owners(self, contract_address, token_id):
        pass

    def get_token_metadata(self, contract_address, token_id):
        pass

    def get_token_uri(self, contract_address, token_id):
        pass

    def get_token_supply(self, contract_address):
        pass

    def get_token_name(self, contract_address):
        pass
