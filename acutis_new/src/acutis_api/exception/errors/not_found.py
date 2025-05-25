from http import HTTPStatus


class HttpNotFoundError(Exception):
    def __init__(self, message: str):
        self.name = 'Not Found'
        self.status_code = HTTPStatus.NOT_FOUND
        self.message = message
