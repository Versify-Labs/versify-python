from versify.paths.v2_assets_asset_id.get import ApiForget
from versify.paths.v2_assets_asset_id.put import ApiForput
from versify.paths.v2_assets_asset_id.delete import ApiFordelete


class V2AssetsAssetId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
