from flask_jwt_extended import current_user

from acutis_api.communication.requests.autenticacao import (
    AlterarSenhaRequest,
)
from acutis_api.domain.repositories.autenticacao import (
    AutenticacaoRepositoryInterface,
)
from acutis_api.exception.errors.unauthorized import HttpUnauthorizedError


class AlterarSenhaUseCase:
    def __init__(
        self, autenticacao_repository: AutenticacaoRepositoryInterface
    ):
        self.__autenticacao_repository = autenticacao_repository

    def execute(self, request: AlterarSenhaRequest):
        senha_atual = request.senha_atual.get_secret_value().strip()
        nova_senha = request.nova_senha.get_secret_value().strip()

        usuario = current_user

        if not usuario.verificar_senha(senha_atual):
            raise HttpUnauthorizedError('A senha atual está incorreta.')

        self.__autenticacao_repository.alterar_senha(usuario, nova_senha)

        self.__autenticacao_repository.salvar_alteracoes()
