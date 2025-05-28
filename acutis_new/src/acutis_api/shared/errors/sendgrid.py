from http import HTTPStatus


class HttpSendGridError(Exception):
    def __init__(self, message: str):
        self.name = 'Erro no SendGrid'
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.message = message
