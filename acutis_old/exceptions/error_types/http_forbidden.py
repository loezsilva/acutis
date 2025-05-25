from http import HTTPStatus


class ForbiddenError(Exception):
    def __init__(self, message: str):
        self.name = "Forbidden"
        self.status_code = HTTPStatus.FORBIDDEN
        self.error_message = message
