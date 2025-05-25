from http import HTTPStatus


class UnauthorizedError(Exception):
    def __init__(self, message: str):
        self.name = "Unauthorized"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.error_message = message
