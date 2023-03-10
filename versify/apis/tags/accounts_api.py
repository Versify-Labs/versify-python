# coding: utf-8

"""
    Versify API

    Versify API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from versify.paths.v2_accounts.post import CreateAccountV2AccountsPost
from versify.paths.v2_accounts_account_id.delete import DeleteAccountV2AccountsAccountIdDelete
from versify.paths.v2_accounts_account_id_metrics.get import GetAccountMetricsV2AccountsAccountIdMetricsGet
from versify.paths.v2_accounts_account_id.get import GetAccountV2AccountsAccountIdGet
from versify.paths.v2_accounts.get import ListAccountsV2AccountsGet
from versify.paths.v2_accounts_account_id.put import UpdateAccountV2AccountsAccountIdPut


class AccountsApi(
    CreateAccountV2AccountsPost,
    DeleteAccountV2AccountsAccountIdDelete,
    GetAccountMetricsV2AccountsAccountIdMetricsGet,
    GetAccountV2AccountsAccountIdGet,
    ListAccountsV2AccountsGet,
    UpdateAccountV2AccountsAccountIdPut,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
