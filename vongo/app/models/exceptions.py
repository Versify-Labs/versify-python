from fastapi import HTTPException
from fastapi import status as http_status


"""
200 - OK - Everything worked as expected.
400 - Bad Request - The request was unacceptable, often due to missing a required parameter.
401 - Unauthorized - No valid API key provided.
402 - Request Failed - The parameters were valid but the request failed.
403 - Forbidden - The API key doesn't have permissions to perform the request.
404 - Not Found	- The requested resource doesn't exist.
409 - Conflict - The request conflicts with another request (perhaps due to using the same idempotent key).
429 - Too Many Requests	- Too many requests hit the API too quickly. We recommend an exponential backoff of your requests.
500, 502, 503, 504 - Server Errors - Something went wrong on Versify's end. (These are rare.)
"""


class BadRequestException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="The request was unacceptable, often due to missing a required parameter.",
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="No valid access token provided.",
        )


class RequestFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_402_REQUEST_FAILED,
            detail="The parameters were valid but the request failed.",
        )


class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="The access token doesn't have permissions to perform the request.",
        )


class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="The requested resource doesn't exist.",
        )


class ConflictException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="The request conflicts with another request.",
        )


class TooManyRequestsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests hit the API too quickly. We recommend an exponential backoff of your requests.",
        )


class ServerErrorException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong on Versify's end.",
        )
