from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    verificar_token,
)
from acutis_api.communication.requests.autenticacao import (
    VerificarTokenRequest,
)
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class VerificarTokenAtivacaoContaUseCase:
    def __init__(self, repository: MembrosRepositoryInterface):
        self.__repository = repository

    def execute(self, requisicao: VerificarTokenRequest) -> dict:
        dados_do_token = verificar_token(
            requisicao.token, TokenSaltEnum.ativar_conta
        )

        busca_lead = self.__repository.buscar_lead_por_email(
            dados_do_token['email']
        )

        if busca_lead is None:
            raise HttpNotFoundError('Usuário não encontrado')

        if busca_lead.ultimo_acesso is not None or (busca_lead.status is True):
            raise HttpConflictError('Conta já está ativa')

        return {'email': dados_do_token['email']}
