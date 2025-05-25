from exceptions.error_types.http_conflict import ConflictError
from models.vocacional.etapa_vocacional import VocationalStepsEnum, VocationalStepsStatusEnum
from models.vocacional.usuario_vocacional import UsuarioVocacional
from repositories.schemas.vocacional_schema import ImageEtapaVocacional
from templates.email_templates import (
    send_cadastro_vocacional,
    send_congratulations_vocacional,
)
from utils.send_email import send_email
from utils.token_email import generate_token

def envia_email_vocacional(vocacional: UsuarioVocacional):
    try:

        payload_vocacional = {"fk_usuario_vocacional_id": vocacional.id}

        token = generate_token(payload_vocacional, salt="decode-token-vocacional")

        if vocacional.status in [VocationalStepsStatusEnum.REPROVADO, VocationalStepsStatusEnum.DESISTENCIA, VocationalStepsStatusEnum.PENDENTE]:
            raise ConflictError(
                "Não foi possível enviar o email pois o processo foi marcado como reprovado ou desistente ou pendente."
            )

        if vocacional.etapa in [VocationalStepsEnum.CADASTRO, VocationalStepsEnum.PRE_CADASTRO]:

            if vocacional.etapa == VocationalStepsEnum.PRE_CADASTRO:
                url_redirect = f"benfeitor/vocacional/cadastro/{token}"
                imagem_etapa = ImageEtapaVocacional.ETAPA_PRE_CADASTRO.value

            if vocacional.etapa == VocationalStepsEnum.CADASTRO:
                url_redirect = f"benfeitor/vocacional/ficha-vocacional/{token}"
                imagem_etapa = ImageEtapaVocacional.ETAPA_CADASTRO.value

            html = send_cadastro_vocacional(
                vocacional.nome,
                url_redirect,
                f"benfeitor/vocacional/desistencia/{token}",
                imagem_etapa
            )

            send_email("Atualização do processo vocacional", vocacional.email, html, 6)

        if vocacional.etapa == VocationalStepsEnum.FICHA_VOCACIONAL and vocacional.status == VocationalStepsStatusEnum.APROVADO:
            html = send_congratulations_vocacional(vocacional.nome, ImageEtapaVocacional.ETAPA_FICHA_VOCACIONAL.value)

            send_email("Processo vocacional finalizado", vocacional.email, html, 6)

        return
    except Exception as e:
        raise e
