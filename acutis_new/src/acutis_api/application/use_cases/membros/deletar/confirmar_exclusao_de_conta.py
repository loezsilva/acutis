from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    verificar_token,
)
from acutis_api.communication.requests.autenticacao import (
    VerificarTokenRequest,
)
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ConfirmaExclusaoContaUseCase:
    def __init__(self, repository: MembrosRepositoryInterface):
        self.__repository = repository

    def execute(self, requisicao: VerificarTokenRequest):
        dados_do_token = verificar_token(
            requisicao.token, TokenSaltEnum.excluir_conta
        )

        busca_lead = self.__repository.buscar_lead_por_email(
            dados_do_token['email']
        )

        if busca_lead is None:
            raise HttpNotFoundError('Usuário não encontrado')

        self.__repository.remove_referencias_lead_id(busca_lead.id)

        self.__repository.excluir_conta(busca_lead)

        self.__repository.salvar_alteracoes()
