"""Can authenticate an API call with a token and account id."""
from ..api.errors import ExpansionDepthError, ExpansionResourceError
from ..services._config import config
from ..utils.mongo import mdb


class ExpandableResource:

    def __init__(self) -> None:
        pass

    def get_resource_obj(self, obj_type, obj_id, account=None):
        resource_cfg = config[obj_type]
        resource_collection = mdb[resource_cfg.db][resource_cfg.collection]
        resource_model = resource_cfg.model

        # Create query params
        query = {'_id': obj_id}
        if account:
            query['account'] = account

        # Find resource in collection
        found = resource_collection.find_one(query)
        if not found:
            return None

        return resource_model(**found).to_json()

    def expand_object(self, data, path=''):
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
        resource_obj = self.get_resource_obj(child_object, resource_id)
        data[child_object] = self.expand_object(resource_obj, next_path)
        return data

    def expand(self, data, expand):
        if type(data) == list:
            data = {'data': data, 'object': 'list'}
        for path in expand:
            if path.startswith('data'):
                new_data = []
                new_path = path[5:]
                for obj in data['data']:  # type: ignore

                    new_data.append(self.expand_object(obj, new_path))
                data['data'] = new_data  # type: ignore
            else:
                data = self.expand_object(data, path)
        return data
