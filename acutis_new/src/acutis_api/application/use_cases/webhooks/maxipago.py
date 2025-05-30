from acutis_api.communication.enums.admin_doacoes import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.webhooks import WebhooksRepositoryInterface
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.templates.email_templates import (
    obrigado_pela_doacao_template,
)


class WebhookMaxiPagoUseCase:
    def __init__(
        self,
        repository: WebhooksRepositoryInterface,
        notification: EnviarNotificacaoInterface,
        file_service: FileServiceInterface,
    ):
        self._repository = repository
        self._notification = notification
        self._file_service = file_service

    def execute(self, request):
        data = request['Request']['transaction-event']
        codigo_ordem_pagamento = data['orderID']
        codigo_referencia = data['referenceNumber']
        codigo_transacao = data['transactionID']

        processamento_doacao = (
            self._repository.buscar_processamento_doacao_por_codigo_transacao(
                codigo_transacao
            )
        )
        if not processamento_doacao:
            pagamento_doacao = (
                self._repository.buscar_pagamento_doacao_por_codigo_ordem(
                    codigo_ordem_pagamento
                )
            )
            if pagamento_doacao:
                status_processamento = (
                    StatusProcessamentoEnum.pago
                    if data['transactionState'] == 'Captured'
                    else StatusProcessamentoEnum.expirado
                )

                processamento_doacao = (
                    self._repository.registrar_novo_processamento_doacao(
                        pagamento_doacao_id=pagamento_doacao.id,
                        codigo_referencia=codigo_referencia,
                        codigo_transacao=codigo_transacao,
                        status_processamento=status_processamento,
                    )
                )
                self._repository.salvar_alteracoes()

                if status_processamento == StatusProcessamentoEnum.pago:
                    dados_doacao = self._repository.buscar_dados_doacao_por_processamento_doacao(  # noqa
                        processamento_doacao
                    )

                    foto_campanha = self._file_service.buscar_url_arquivo(
                        dados_doacao.foto_campanha
                    )
                    conteudo = obrigado_pela_doacao_template(
                        dados_doacao.nome,
                        dados_doacao.nome_campanha,
                        foto_campanha,
                    )

                    self._notification.enviar_email(
                        dados_doacao.email,
                        AssuntosEmailEnum.agradecimento_doacao,
                        conteudo,
                    )
