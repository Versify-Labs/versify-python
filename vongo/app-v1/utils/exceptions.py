from http import HTTPStatus


class ServiceError(Exception):
    """API Gateway Service Error"""

    def __init__(self, status_code: int, msg: str):
        """
        Parameters
        ----------
        status_code: int
            Http status code
        msg: str
            Error message
        """
        self.status_code = status_code
        self.msg = msg


class BadRequestError(ServiceError):
    """API Gateway Bad Request Error (400)"""

    def __init__(self, msg: str):
        super().__init__(HTTPStatus.BAD_REQUEST, msg)


class UnauthorizedError(ServiceError):
    """API Gateway Unauthorized Error (401)"""

    def __init__(self, msg: str):
        super().__init__(HTTPStatus.UNAUTHORIZED, msg)


class NotFoundError(ServiceError):
    """API Gateway Not Found Error (404)"""

    def __init__(self, msg: str = "Not found"):
        super().__init__(HTTPStatus.NOT_FOUND, msg)


class InternalServerError(ServiceError):
    """API Gateway Not Found Internal Server Error (500)"""

    def __init__(self, message: str):
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, message)


class ExpansionDepthError(BadRequestError):
    def __init__(self):
        msg = "Expansions have a maximum depth of four levels."
        super().__init__(msg)


class ExpansionResourceError(BadRequestError):
    def __init__(self, parent, child):
        msg = f"The {child} resource cannot be expanded on a {parent}."
        super().__init__(msg)


class UsageLimitError(BadRequestError):
    def __init__(self):
        msg = "Limit exceeded."
        super().__init__(msg)
