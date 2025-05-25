from http import HTTPStatus


class ConflictError(Exception):
    def __init__(self, message: str):
        self.name = "Conflict"
        self.status_code = HTTPStatus.CONFLICT
        self.error_message = message
