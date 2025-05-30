from http import HTTPStatus

from acutis_api.communication.requests.agape import (
    RegistrarNomeAcaoAgapeFormData,
)
from acutis_api.communication.responses.agape import (
    RegistrarAcaoAgapeResponse,
)
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarNomeAcaoAgapeUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__agape_repository = agape_repository

    def execute(
        self, dados: RegistrarNomeAcaoAgapeFormData
    ) -> tuple[dict, HTTPStatus]:
        verifica_nome_campanha_ja_cadastrado = (
            self.__agape_repository.verificar_nome_da_acao(dados.nome)
        )

        if verifica_nome_campanha_ja_cadastrado is not None:
            raise HttpConflictError('Nome da ação já cadastrado')

        acao = self.__agape_repository.registrar_nome_acao_agape(dados=dados)

        self.__agape_repository.salvar_alteracoes()

        response = RegistrarAcaoAgapeResponse.model_validate(acao).model_dump()

        return response
