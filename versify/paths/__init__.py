# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from versify.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V2_ACCOUNTS = "/v2/accounts"
    V2_ACCOUNTS_ACCOUNT_ID = "/v2/accounts/{account_id}"
    V2_ACCOUNTS_ACCOUNT_ID_METRICS = "/v2/accounts/{account_id}/metrics"
