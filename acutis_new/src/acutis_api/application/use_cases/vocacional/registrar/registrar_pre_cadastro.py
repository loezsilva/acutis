from flask import request

from acutis_api.communication.requests.vocacional import (
    RegistrarPreCadastroRequest,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.domain.services.enviar_notificacao import (
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    send_email_pre_cadastro_vocacional_recebido,
)
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarPreCadastroUseCase:
    def __init__(
        self,
        vocacional_repository: InterfaceVocacionalRepository,
        notification: EnviarNotificacaoInterface,
    ):
        self.__vocacional_repository = vocacional_repository
        self._notification = notification

    def execute(self):
        data_pre_cadastro = RegistrarPreCadastroRequest.model_validate(
            request.get_json()
        )

        email_used = self.__vocacional_repository.verificar_usuario_vocacional_por_email(  # noqa: E501
            data_pre_cadastro
        )

        if email_used is not None:
            raise HttpConflictError('Email já cadastrado')

        pre_cadastro = self.__vocacional_repository.pre_cadastro_vocacional(
            data_pre_cadastro
        )
        self.__vocacional_repository.salvar_alteracoes()

        html_pre_cadastro_recebido = (
            send_email_pre_cadastro_vocacional_recebido(pre_cadastro.nome)
        )
        self._notification.enviar_email(
            pre_cadastro.email,
            'Recebemos seu cadastro no processo vocacional',
            html_pre_cadastro_recebido,
        )
