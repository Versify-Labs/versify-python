from versify.paths.v2_accounts_account_id.get import ApiForget
from versify.paths.v2_accounts_account_id.put import ApiForput
from versify.paths.v2_accounts_account_id.delete import ApiFordelete


class V2AccountsAccountId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
