from http import HTTPStatus


class HttpUnauthorizedError(Exception):
    def __init__(self, message: str):
        self.name = 'Unauthorized'
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.message = message
