import typing_extensions

from versify.apis.tags import TagValues
from versify.apis.tags.assets_api import AssetsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ASSETS: AssetsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ASSETS: AssetsApi,
    }
)
