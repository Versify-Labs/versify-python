# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from versify.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    V2_ASSETS = "/v2/assets"
    V2_ASSETS_SEARCH = "/v2/assets/search"
    V2_ASSETS_ASSET_ID = "/v2/assets/{asset_id}"
