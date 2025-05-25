from http import HTTPStatus


class HttpForbiddenError(Exception):
    def __init__(self, message: str):
        self.name = 'Forbidden'
        self.status_code = HTTPStatus.FORBIDDEN
        self.message = message
