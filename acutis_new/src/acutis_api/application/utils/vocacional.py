from acutis_api.application.utils.funcoes_auxiliares import gerar_token
from acutis_api.communication.enums.vocacional import (
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.etapa_vocacional import EtapaVocacional
from acutis_api.domain.entities.usuario_vocacional import UsuarioVocacional
from acutis_api.domain.templates.email_templates import (
    send_cadastro_vocacional,
    send_congratulations_vocacional,
)
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.infrastructure.services.sendgrid import SendGridService


def envia_email_vocacional(vocacional: UsuarioVocacional):
    notification = SendGridService()

    payload_vocacional = {'fk_usuario_vocacional_id': str(vocacional.id)}
    token = gerar_token(payload_vocacional, salt='decode-token-vocacional')
    if vocacional.status in {
        PassosVocacionalStatusEnum.reprovado,
        PassosVocacionalStatusEnum.desistencia,
    }:
        raise HttpConflictError(
            'Não foi possível enviar o email \
                pois o processo foi marcado como reprovado ou desistente.'
        )

    if vocacional.etapa in {
        PassosVocacionalEnum.cadastro,
        PassosVocacionalEnum.pre_cadastro,
    }:
        if vocacional.etapa == PassosVocacionalEnum.pre_cadastro:
            url_redirect = f'benfeitor/vocacional/cadastro/{token}'

        if vocacional.etapa == PassosVocacionalEnum.cadastro:
            url_redirect = f'benfeitor/vocacional/ficha-vocacional/{token}'

        html = send_cadastro_vocacional(
            vocacional.nome,
            url_redirect,
            f'benfeitor/vocacional/desistencia/{token}',
        )

        notification.enviar_email(
            vocacional.email, 'Atualização do processo vocacional', html
        )

    if (
        vocacional.etapa == PassosVocacionalEnum.ficha_vocacional
        and vocacional.status == PassosVocacionalStatusEnum.aprovado
    ):
        html = send_congratulations_vocacional(vocacional.nome)

        notification.enviar_email(
            vocacional.email, 'Atualização do processo vocacional', html
        )


def verifica_etapa_aprovada(pre_cadastro: EtapaVocacional, etapa: str):
    if pre_cadastro.status == PassosVocacionalStatusEnum.desistencia:
        raise HttpConflictError(
            'Não é possível prosseguir pois encontramos \
                um registro de desistência no seu processo vocacional.'
        )

    if pre_cadastro.status == PassosVocacionalStatusEnum.pendente:
        raise HttpConflictError(
            f'É necessário ter o {etapa} aprovado para continuar.'
        )

    if pre_cadastro.status == PassosVocacionalStatusEnum.reprovado:
        raise HttpConflictError(
            'Não é possível prosseguir pois seu cadastrado \
                foi marcado como recusado anteriomente.'
        )
