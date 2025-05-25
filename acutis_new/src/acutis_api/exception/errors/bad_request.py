from http import HTTPStatus


class HttpBadRequestError(Exception):
    def __init__(self, message: str):
        self.name = 'Bad Request'
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = message
