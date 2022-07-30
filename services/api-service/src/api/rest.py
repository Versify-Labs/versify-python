from typing import Optional

from aws_lambda_powertools.event_handler import APIGatewayRestResolver


class Request:

    def __init__(self, app: APIGatewayRestResolver, id: Optional[str] = None):
        self._id = id
        self._path = app.current_event.path

        # Add context data
        self._account = app.current_event.get_header_value('Versify-Account')
        self._email = None
        self._user = None
        authorizer = {}
        try:
            authorizer = app.current_event.request_context.authorizer or {}
            self._account = authorizer.get('account')
            self._email = authorizer.get('email')
            self._user = authorizer.get('user')
        except:
            authorizer = {}

        # Construct body
        self._body = {}
        if app.current_event.body:
            self._body = app.current_event.json_body

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
        if self._account:
            self._filter['account'] = self._account

    @property
    def account(self) -> Optional[str]:
        return self._account

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
            'expand_list': self._expand_list,
            'auth': {
                'account': self._account,
                'email': self._email,
                'user': self._user
            }
        }

    @property
    def delete(self) -> dict:
        return {
            'filter': self._filter
        }

    @property
    def filter(self) -> dict:
        return self._filter

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
    def path(self) -> str:
        return self._path

    @property
    def update(self) -> dict:
        return {
            'body': self._body,
            'filter': self._filter,
            'expand_list': self._expand_list
        }

    @property
    def user(self) -> Optional[str]:
        return self._user

    @body.setter
    def body(self, value):
        self._body = value

    @body.setter
    def filter(self, value):
        self._filter = value


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
        self.account = req.account
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
