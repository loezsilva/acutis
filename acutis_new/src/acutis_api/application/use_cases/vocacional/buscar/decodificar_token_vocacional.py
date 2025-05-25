from acutis_api.application.utils.funcoes_auxiliares import verificar_token
from acutis_api.communication.responses.vocacional import (
    DecodificarTokenVocacionalResponse,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.exception.errors_handler import HttpNotFoundError


class DecodificarTokenVocacionalUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, token: str):
        data_token_decodificado = verificar_token(
            token, 'decode-token-vocacional'
        )
        resultado = self.__vocacional_repository.busca_info_token(
            data_token_decodificado
        )

        if resultado is None:
            raise HttpNotFoundError('Vocacional não encontrado.')

        response = DecodificarTokenVocacionalResponse.model_validate(
            resultado
        ).model_dump()

        return response
