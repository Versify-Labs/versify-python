from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError


class ExpansionDepthError(BadRequestError):

    def __init__(self):
        msg = 'Expansions have a maximum depth of four levels.'
        super().__init__(msg)


class ExpansionResourceError(BadRequestError):

    def __init__(self, parent, child):
        msg = f'The {child} resource cannot be expanded on a {parent}.'
        super().__init__(msg)


class UsageLimitError(BadRequestError):

    def __init__(self):
        msg = 'Account usage limit reached for this request.'
        super().__init__(msg)
