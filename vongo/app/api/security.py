from typing import Optional

from fastapi.openapi.models import HTTPBase as HTTPBaseModel
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.openapi.models import SecuritySchemeType
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from .exceptions import ForbiddenException
from .models import HTTPAuthorizationCredentials


class HTTPBase(SecurityBase):
    def __init__(
        self,
        *,
        scheme: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBaseModel(
            scheme=scheme,
            description=description,
            type=SecuritySchemeType.http,
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise ForbiddenException()
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, token=credentials)


class HTTPBearer(HTTPBase):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = HTTPBearerModel(
            bearerFormat=bearerFormat,
            description=description,
            type=SecuritySchemeType.http,
            scheme="bearer",
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise ForbiddenException()
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                ForbiddenException("Invalid authorization scheme")
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, token=credentials)
