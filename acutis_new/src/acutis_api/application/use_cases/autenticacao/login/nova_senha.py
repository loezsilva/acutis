from pwdlib import PasswordHash

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    verificar_token,
)
from acutis_api.communication.requests.autenticacao import (
    NovaSenhaQuery,
    NovaSenhaRequest,
)
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class NovaSenhaUseCase:
    def __init__(
        self,
        membros_repository: MembrosRepositoryInterface,
    ) -> None:
        self.__membros_repository = membros_repository

    def execute(self, request: NovaSenhaRequest, query_params: NovaSenhaQuery):
        pwd_context = PasswordHash.recommended()

        nova_senha = request.nova_senha.get_secret_value().strip()
        token = query_params.token
        usuario = verificar_token(
            token, salt=TokenSaltEnum.recuperar_senha, max_age=1 * 60 * 60
        )
        email = usuario.get('email')
        usuario = self.__membros_repository.buscar_lead_por_email(email)
        if usuario is None:
            raise HttpNotFoundError('Usuário não encontrado')

        if usuario.status is not False:
            self.__membros_repository.ativa_conta_com_senha(
                pwd_context.hash(nova_senha), usuario
            )
            self.__membros_repository.salvar_alteracoes()
            return

        self.__membros_repository.alterar_senha(usuario, nova_senha)
        self.__membros_repository.salvar_alteracoes()
