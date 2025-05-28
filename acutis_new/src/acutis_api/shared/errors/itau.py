from http import HTTPStatus


class ItauHttpBadRequestError(Exception):
    def __init__(self, message: str):
        self.name = 'Erro no Itau Gateway'
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = message
