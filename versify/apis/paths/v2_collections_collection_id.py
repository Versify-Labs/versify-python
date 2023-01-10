from versify.paths.v2_collections_collection_id.get import ApiForget
from versify.paths.v2_collections_collection_id.put import ApiForput
from versify.paths.v2_collections_collection_id.delete import ApiFordelete


class V2CollectionsCollectionId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
