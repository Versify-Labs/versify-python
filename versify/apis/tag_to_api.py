import typing_extensions

from versify.apis.tags import TagValues
from versify.apis.tags.accounts_api import AccountsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCOUNTS: AccountsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCOUNTS: AccountsApi,
    }
)
