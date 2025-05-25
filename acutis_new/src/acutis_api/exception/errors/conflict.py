from http import HTTPStatus


class HttpConflictError(Exception):
    def __init__(self, message: str):
        self.name = 'Conflict'
        self.status_code = HTTPStatus.CONFLICT
        self.message = message
