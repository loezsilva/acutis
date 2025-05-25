from http import HTTPStatus


class HttpUnprocessableEntity(Exception):
    def __init__(self, message: str):
        self.name = "Unprocessable Entity"
        self.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        self.error_message = message
