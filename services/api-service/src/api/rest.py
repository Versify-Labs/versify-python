from typing import Optional

from aws_lambda_powertools.event_handler import APIGatewayRestResolver


class Request:

    def __init__(self, app: APIGatewayRestResolver, id: Optional[str] = None):
        self._id = id
        self._org = app.current_event.get_header_value('X-Organization')
        self._path = app.current_event.path

        # Construct body
        self._body = {}
        if app.current_event.body:
            self._body = app.current_event.json_body
        if self.org:
            self._body['organization'] = self.org

        # Cleanup query params from request
        query_params = {}
        query_dict = app.current_event.query_string_parameters or {}
        for k, v in query_dict.items():
            if v == 'true':
                v = True
            if v == 'false':
                v = False
            query_params[k] = v

        # Construct expand list
        self._expand_list = query_params.pop('expand', '').split(',')

        # Construct limit and skip
        page_size = int(query_params.pop('page_size', 20))
        page_num = int(query_params.pop('page_num', 1))
        self._limit = page_size
        self._skip = page_size * (page_num - 1)

        # Construct filter starting with leftover query params
        self._filter = query_params

        # Construct rest of filter from filter param
        filter_param = query_params.pop('filter', '').split(',')
        filter_list = [f for f in filter_param if f.count('-') == 2]
        for f in filter_list:
            prop, op, val = f.split('-')
            if op == 'equal':
                self._filter[prop] = {'$eq': val}  # type: ignore
            elif op == 'notEqual':
                self._filter[prop] = {'$ne': val}  # type: ignore
            elif op == 'contains':
                self._filter[prop] = {'$regex': val}  # type: ignore
            elif op == 'greaterThan':
                self._filter[prop] = {'$gt': val}  # type: ignore
            elif op == 'lessThan':
                self._filter[prop] = {'$lt': val}  # type: ignore
            elif op == 'isBlank':
                self._filter[prop] = {'$exists': False}  # type: ignore
            elif op == 'isPresent':
                self._filter[prop] = {'$exists': True}  # type: ignore

        # Other Params
        if id:
            self._filter['_id'] = id
        if self._org:
            self._filter['organization'] = self._org

    @property
    def body(self) -> dict:
        return self._body

    @property
    def count(self) -> dict:
        return {
            'filter': self._filter
        }

    @property
    def create(self) -> dict:
        return {
            'body': self._body,
            'expand_list': self._expand_list
        }

    @property
    def delete(self) -> dict:
        return {
            'filter': self._filter
        }

    @property
    def get(self) -> dict:
        return {
            'expand_list': self._expand_list,
            'filter': self._filter,
        }

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def list(self) -> dict:
        return {
            'expand_list': self._expand_list,
            'filter': self._filter,
            'limit': self._limit,
            'skip': self._skip,
        }

    @property
    def org(self) -> Optional[str]:
        return self._org

    @property
    def path(self) -> str:
        return self._path

    @property
    def update(self) -> dict:
        return {
            'body': self._body,
            'filter': self._filter,
            'expand_list': self._expand_list
        }

    @body.setter
    def body(self, value):
        self._body = value


class Response:

    def __init__(
        self,
        req: Request,
        data=None,
        count=None
    ):
        self.count = count
        self.data = data

        # Construct has_more from data
        self.has_more = False
        if data and count:
            self.has_more = count > len(data)

        # Construct variables from req object
        self.id = req.id
        self.org = req.org
        self.url = req.path

        # Construct object from request object
        self.object = None
        if isinstance(data, dict):
            self.object = data['object']
        elif isinstance(data, list) and len(data) > 0:
            self.object = data[0]['object']

    @property
    def create(self) -> Optional[dict]:
        return self.data

    @property
    def delete(self) -> dict:
        return {
            'id': self.id,
            'object': self.object,
            'deleted': True
        }

    @property
    def get(self) -> Optional[dict]:
        return self.data

    @property
    def list(self) -> dict:
        return {
            'object': 'list',
            'url': self.url,
            'has_more': self.has_more,
            'data': self.data,
            'count': self.count
        }

    @property
    def update(self) -> Optional[dict]:
        return self.data
