import typing_extensions

from versify.paths import PathValues
from versify.apis.paths.v2_assets import V2Assets
from versify.apis.paths.v2_assets_search import V2AssetsSearch
from versify.apis.paths.v2_assets_asset_id import V2AssetsAssetId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.V2_ASSETS: V2Assets,
        PathValues.V2_ASSETS_SEARCH: V2AssetsSearch,
        PathValues.V2_ASSETS_ASSET_ID: V2AssetsAssetId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.V2_ASSETS: V2Assets,
        PathValues.V2_ASSETS_SEARCH: V2AssetsSearch,
        PathValues.V2_ASSETS_ASSET_ID: V2AssetsAssetId,
    }
)
