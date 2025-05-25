from http import HTTPStatus
from models.schemas.vocacional.get.decodificar_token_vocacional_schema import (
    DecodificarTokenVocacionalResponse,
)
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)
from utils.token_email import verify_token


class DecodificarTokenVocacional:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, token: str):
        data_decode_token = verify_token(token, "decode-token-vocacional")
        result = self.__vocacional_repository.get_info_token(data_decode_token)

        response = DecodificarTokenVocacionalResponse.from_orm(result).dict()

        return response, HTTPStatus.OK
