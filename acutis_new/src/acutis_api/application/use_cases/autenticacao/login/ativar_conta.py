from flask import jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from pwdlib import PasswordHash

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    verificar_token,
)
from acutis_api.communication.requests.autenticacao import (
    AtivarContaRequest,
    UsarHttpOnlyQuery,
)
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AtivarContaUseCase:
    def __init__(self, repository: MembrosRepositoryInterface):
        self.__repository = repository

    def execute(
        self, requisicao: AtivarContaRequest, query: UsarHttpOnlyQuery
    ):
        pwd_context = PasswordHash.recommended()

        token_decriptado = verificar_token(
            requisicao.token, TokenSaltEnum.ativar_conta
        )

        busca_lead = self.__repository.buscar_lead_por_email(
            token_decriptado['email']
        )

        if busca_lead is None:
            raise HttpNotFoundError('Usuário não encontrado')

        if busca_lead.ultimo_acesso is not None or busca_lead.status is True:
            raise HttpConflictError('Conta já está ativa')

        self.__repository.ativa_conta_com_senha(
            pwd_context.hash(requisicao.senha.get_secret_value()), busca_lead
        )

        self.__repository.atualizar_data_ultimo_acesso(busca_lead)
        self.__repository.salvar_alteracoes()

        access_token = create_access_token(identity=busca_lead.id)
        refresh_token = create_refresh_token(identity=busca_lead.id)

        if query.httponly:
            response = make_response()
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
        else:
            response = jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'msg': 'Conta ativada com sucesso',
            })

        return response
