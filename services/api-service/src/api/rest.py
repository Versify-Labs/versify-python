from typing import Optional

from aws_lambda_powertools.event_handler import APIGatewayRestResolver


class BaseRequest:
    def __init__(self, app: APIGatewayRestResolver, id: Optional[str] = None):
        self._id = id
        self._path = app.current_event.path

        # Construct body
        self._body = {}
        if app.current_event.body:
            self._body = app.current_event.json_body

        # Cleanup query params from request
        query_params = {}
        query_dict = app.current_event.query_string_parameters or {}
        for k, v in query_dict.items():
            if v == "true":
                v = True
            if v == "false":
                v = False
            query_params[k] = v

        # Construct expand list
        self._expand_list = query_params.pop("expand", "").split(",")

        # Construct limit and skip
        page_size = int(query_params.pop("page_size", 20))
        page_num = int(query_params.pop("page_num", 1))
        self._limit = page_size
        self._skip = page_size * (page_num - 1)

        # Construct filter starting with leftover query params
        self._filter = query_params

        # Construct rest of filter from filter param
        filter_param = query_params.pop("filter", "").split(",")
        filter_list = [f for f in filter_param if f.count("-") == 2]
        for f in filter_list:
            prop, op, val = f.split("-")
            if op == "equal":
                self._filter[prop] = {"$eq": val}  # type: ignore
            elif op == "notEqual":
                self._filter[prop] = {"$ne": val}  # type: ignore
            elif op == "contains":
                self._filter[prop] = {"$regex": val}  # type: ignore
            elif op == "greaterThan":
                self._filter[prop] = {"$gt": val}  # type: ignore
            elif op == "lessThan":
                self._filter[prop] = {"$lt": val}  # type: ignore
            elif op == "isBlank":
                self._filter[prop] = {"$exists": False}  # type: ignore
            elif op == "isPresent":
                self._filter[prop] = {"$exists": True}  # type: ignore

        # Other Params
        if id:
            self._filter["_id"] = id

    @property
    def body(self) -> dict:
        return self._body

    @property
    def expand_list(self) -> Optional[list]:
        return self._expand_list

    @property
    def filter(self) -> dict:
        return self._filter

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def path(self) -> str:
        return self._path

    @property
    def skip(self) -> int:
        return self._skip

    @body.setter
    def body(self, value):
        self._body = value

    @filter.setter
    def filter(self, value):
        self._filter = value


class AccountRequest(BaseRequest):
    def __init__(self, app: APIGatewayRestResolver, id: Optional[str] = None):
        super().__init__(app, id)
        authorizer = app.current_event.request_context.authorizer or {}
        self._account = authorizer["account"]
        self._email = authorizer.get("email")
        self._role = authorizer.get("role")
        self._user = authorizer.get("user")
        self._filter["account"] = self._account

    @property
    def account(self) -> Optional[str]:
        return self._account

    @property
    def email(self) -> Optional[str]:
        return self._email

    @property
    def role(self) -> Optional[str]:
        return self._role

    @property
    def user(self) -> Optional[str]:
        return self._user


class UserRequest(BaseRequest):
    def __init__(self, app: APIGatewayRestResolver, id: Optional[str] = None):
        super().__init__(app, id)
        authorizer = app.current_event.request_context.authorizer or {}
        self._email = authorizer["email"]
        self._user = authorizer["user"]

    @property
    def email(self) -> Optional[str]:
        return self._email

    @property
    def user(self) -> Optional[str]:
        return self._user


class PublicRequest(BaseRequest):
    def __init__(self, app: APIGatewayRestResolver, id: Optional[str] = None):
        super().__init__(app, id)


class BaseResponse:
    def __init__(self, req: BaseRequest, data=None, count=None):
        self.req = req
        self.count = count
        self.data = data

        # Construct has_more from data
        self.has_more = False
        if data and count:
            self.has_more = count > len(data)

        # Construct variables from req object
        self.id = req.id
        self.url = req.path

        # Construct object from request object
        self.object = None
        if isinstance(data, dict):
            self.object = data["object"]
        elif isinstance(data, list) and len(data) > 0:
            self.object = data[0]["object"]


class CreateResponse(BaseResponse):
    def __init__(self, req: BaseRequest, data: dict):
        super().__init__(req, data=data)

    @property
    def json(self) -> Optional[dict]:
        return self.data


class DeleteResponse(BaseResponse):
    def __init__(self, req: BaseRequest):
        super().__init__(req)

    @property
    def json(self) -> dict:
        return {"id": self.id, "object": self.object, "deleted": True}


class GetResponse(BaseResponse):
    def __init__(self, req: BaseRequest, data: dict):
        super().__init__(req, data=data)

    @property
    def json(self) -> Optional[dict]:
        return self.data


class ListResponse(BaseResponse):
    def __init__(self, req: BaseRequest, data: list, count: int):
        super().__init__(req, data=data, count=count)

    @property
    def json(self) -> dict:
        return {
            "object": "list",
            "url": self.url,
            "has_more": self.has_more,
            "data": self.data,
            "count": self.count,
        }


class UpdateResponse(BaseResponse):
    def __init__(self, req: BaseRequest, data: dict):
        super().__init__(req, data=data)

    @property
    def json(self) -> Optional[dict]:
        return self.data
