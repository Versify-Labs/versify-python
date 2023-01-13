import typing_extensions

from versify.paths import PathValues
from versify.apis.paths.v2_accounts import V2Accounts
from versify.apis.paths.v2_accounts_account_id import V2AccountsAccountId
from versify.apis.paths.v2_accounts_account_id_metrics import V2AccountsAccountIdMetrics

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V2_ACCOUNTS: V2Accounts,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID: V2AccountsAccountId,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID_METRICS: V2AccountsAccountIdMetrics,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V2_ACCOUNTS: V2Accounts,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID: V2AccountsAccountId,
        PathValues.V2_ACCOUNTS_ACCOUNT_ID_METRICS: V2AccountsAccountIdMetrics,
    }
)
