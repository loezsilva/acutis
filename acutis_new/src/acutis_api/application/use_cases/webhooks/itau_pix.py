from acutis_api.domain.repositories.schemas.webhooks import (
    RegistrarDoacaoAnonimaSchema,
)
from acutis_api.domain.repositories.webhooks import WebhooksRepositoryInterface
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.domain.templates.email_templates import (
    obrigado_pela_doacao_template,
)


class WebhookItauPixUseCase:
    def __init__(
        self,
        repository: WebhooksRepositoryInterface,
        itau_api: GatewayPagamentoInterface,
        notification: EnviarNotificacaoInterface,
        file_service: FileServiceInterface,
    ):
        self._repository = repository
        self._itau_api = itau_api
        self._notification = notification
        self._file_service = file_service

    def execute(self, request):
        data = request['pix'][0]

        doacao_anonima = data[
            'componentesValor'
        ]  # Se não existir o campo "original" dentro de "componentesValor", a doação é anonima. # noqa
        if doacao_anonima in {None, 'None'}:
            self._registrar_doacao_anonima_benfeitor(data)
        else:
            self._registrar_doacao_membro_benfeitor(data)

    def _registrar_doacao_anonima_benfeitor(self, data: dict):  # noqa
        codigo_comprovante = data['endToEndId']
        chave_pix = data['chave']

        response = self._itau_api.buscar_lancamentos_pix(
            codigo_comprovante, chave_pix
        )

        payload = response['data']
        if len(payload) == 0:
            raise Exception(  # NOSONAR
                'Pagamento ainda não registrado na API do Itau.'
            )

        payload_usuario = payload[0]['detalhe_pagamento']['debitado']
        payload_pagamento = payload[0]['detalhe_pagamento']
        payload_valor = payload[0]['detalhe_pagamento']['detalhe_valor']

        numero_documento = payload_usuario['numero_documento']
        nome = payload_usuario['nome']
        data_pagamento = payload_pagamento['data']
        valor_pagamento = payload_valor['valor']
        codigo_transacao = payload['detalhe_pagamento'].get(
            'id_lancamento', None
        )

        campanha_doacao = (
            self._repository.buscar_campanha_doacao_por_chave_pix(chave_pix)
        )
        campanha_doacao_id = campanha_doacao.id if campanha_doacao else None

        benfeitor = self._repository.buscar_benfeitor_por_numero_documento(
            numero_documento
        )
        if not benfeitor:
            benfeitor = self._repository.registrar_benfeitor(
                nome,
                numero_documento,
            )

        dados_doacao = RegistrarDoacaoAnonimaSchema(
            benfeitor_id=benfeitor.id,
            campanha_doacao_id=campanha_doacao_id,
            valor_pagamento=valor_pagamento,
            data_pagamento=data_pagamento,
            codigo_transacao=codigo_transacao,
            codigo_comprovante=codigo_comprovante,
        )

        self._repository.registrar_doacao_anonima(dados_doacao)

        self._repository.salvar_alteracoes()

    def _registrar_doacao_membro_benfeitor(self, data: dict):
        codigo_transacao = data['txid']
        codigo_comprovante = data['endToEndId']

        processamento_doacao = (
            self._repository.buscar_processamento_doacao_por_codigo_transacao(
                codigo_transacao
            )
        )
        if (
            processamento_doacao
            and not processamento_doacao.codigo_comprovante
        ):
            self._repository.atualizar_status_processamento_doacao(
                processamento_doacao, codigo_comprovante
            )
            self._repository.salvar_alteracoes()

            dados_doacao = (
                self._repository.buscar_dados_doacao_por_processamento_doacao(
                    processamento_doacao
                )
            )

            foto_campanha = self._file_service.buscar_url_arquivo(
                dados_doacao.foto_campanha
            )
            conteudo = obrigado_pela_doacao_template(
                dados_doacao.nome, dados_doacao.nome_campanha, foto_campanha
            )

            self._notification.enviar_email(
                dados_doacao.email,
                AssuntosEmailEnum.agradecimento_doacao,
                conteudo,
            )
