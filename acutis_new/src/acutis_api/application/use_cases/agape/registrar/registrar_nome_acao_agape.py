from acutis_api.application.utils.funcoes_auxiliares import normalizar_texto
from acutis_api.communication.requests.agape import (
    RegistrarNomeAcaoAgapeRequest,
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

    def execute(self, dados: RegistrarNomeAcaoAgapeRequest) -> None:
        nome_acao_normalizado = normalizar_texto(dados.nome)

        verifica_nome_campanha_ja_cadastrado = (
            self.__agape_repository.verificar_nome_da_acao(
                nome_acao_normalizado
            )
        )

        if verifica_nome_campanha_ja_cadastrado is not None:
            raise HttpConflictError('Nome da ação já cadastrado')

        self.__agape_repository.registrar_nome_acao_agape(
            nome_acao=nome_acao_normalizado
        )

        self.__agape_repository.salvar_alteracoes()
