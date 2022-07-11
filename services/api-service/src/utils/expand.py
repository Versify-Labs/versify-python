from ..api.config import config
from ..api.errors import ExpansionDepthError, ExpansionResourceError
from ..utils.mongo import mdb


def get_resource_obj(obj_type, obj_id, organization=None):
    resource_cfg = config[obj_type]
    resource_collection = mdb[resource_cfg.db][resource_cfg.collection]
    resource_model = resource_cfg.model

    # Create query params
    query = {'_id': obj_id}
    if organization:
        query['organization'] = organization

    # Find resource in collection
    found = resource_collection.find_one(query)
    if not found:
        return None

    return resource_model(**found).to_json()


def expand_object(data, path=''):
    resources_left = path.split('.')

    # Base Case
    if len(resources_left) < 1 or resources_left == ['']:
        return data

    # Depth Limit
    if len(resources_left) > 4:
        raise ExpansionDepthError

    # Validate the resource requested can be expanded
    parent_object = data['object']
    child_object = resources_left[0]
    cfg = config[parent_object]
    if child_object not in cfg.expandables:
        raise ExpansionResourceError(parent_object, child_object)

    resource_id = data[child_object]
    if type(resource_id) != str:
        return data

    next_path = '.'.join(resources_left[1:])
    resource_obj = get_resource_obj(child_object, resource_id)
    data[child_object] = expand_object(resource_obj, next_path)
    return data
