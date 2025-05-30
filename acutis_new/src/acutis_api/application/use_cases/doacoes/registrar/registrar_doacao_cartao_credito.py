from datetime import datetime

from acutis_api.application.use_cases.doacoes.registrar import (
    BaseRegistrarDoacaoUseCase,
)
from acutis_api.application.utils.funcoes_auxiliares import formatar_string
from acutis_api.communication.requests.doacoes import (
    RegistrarDoacaoCartaoCreditoRequest,
)
from acutis_api.domain.entities import Campanha, Lead
from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
)
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.domain.repositories.schemas.doacoes import (
    RegistrarDoacaoSchema,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.schemas.maxipago import DadosPagamento
from acutis_api.domain.templates.email_templates import (
    obrigado_pela_doacao_template,
)
from acutis_api.infrastructure.services.maxipago import MaxiPago


class RegistrarDoacaoCartaoCreditoUseCase(BaseRegistrarDoacaoUseCase):
    def __init__(
        self,
        repository: DoacoesRepositoryInterface,
        maxipago: MaxiPago,
        file_service: FileServiceInterface,
        notification: EnviarNotificacaoInterface,
    ):
        super().__init__(repository)
        self._repository = repository
        self._maxipago = maxipago
        self._file_service = file_service
        self._notification = notification

    def execute(
        self, request: RegistrarDoacaoCartaoCreditoRequest, lead: Lead
    ):
        self._validar_lead(lead)
        campanha = self._buscar_campanha(request.campanha_id)
        self._vincular_ou_registrar_benfeitor(lead)

        self._realizar_doacao(request, campanha, lead)

        self._enviar_email_agradecimento(campanha, lead)

    def _realizar_doacao(
        self,
        request: RegistrarDoacaoCartaoCreditoRequest,
        campanha: Campanha,
        lead: Lead,
    ):
        codigo_referencia = f'{lead.membro.benfeitor.id}_CARTAO_{
            datetime.timestamp(datetime.now())
        }'
        dados_pagamento = DadosPagamento(
            codigo_referencia=codigo_referencia,
            numero_documento=request.numero_documento,
            nome=request.nome_titular,
            rua=formatar_string(lead.membro.endereco.logradouro),
            bairro=formatar_string(lead.membro.endereco.bairro),
            cidade=formatar_string(lead.membro.endereco.cidade),
            estado=formatar_string(lead.membro.endereco.estado),
            cep=lead.membro.endereco.codigo_postal,
            telefone=lead.telefone,
            email=lead.email,
            numero_cartao=request.numero_cartao,
            vencimento_mes=request.vencimento_mes,
            vencimento_ano=request.vencimento_ano,
            codigo_seguranca=request.codigo_seguranca,
            valor_doacao=request.valor_doacao,
        )
        if request.recorrente:
            pagamento_response = self._maxipago.criar_pagamento_recorrente(
                dados_pagamento
            )
        else:
            pagamento_response = self._maxipago.criar_pagamento_unico(
                dados_pagamento
            )

        dados_doacao = RegistrarDoacaoSchema(
            benfeitor_id=lead.membro.benfeitor.id,
            campanha_doacao_id=campanha.campanha_doacao.id,
            valor_doacao=request.valor_doacao,
            recorrente=request.recorrente,
            forma_pagamento=FormaPagamentoEnum.credito,
            codigo_ordem_pagamento=pagamento_response.orderID,
            anonimo=False,
            gateway=GatewayPagamentoEnum.maxipago,
            codigo_referencia=pagamento_response.referenceNum,
            codigo_transacao=pagamento_response.transactionID,
            processado_em=datetime.now(),
            status=StatusProcessamentoEnum.pago,
        )
        self._repository.registrar_doacao(dados_doacao)

        try:
            self._repository.salvar_alteracoes()
        except Exception as exc:
            self._maxipago.estornar_pagamento(
                pagamento_response.orderID,
                pagamento_response.referenceNum,
                request.valor_doacao,
            )

            if request.recorrente:
                self._maxipago.cancelar_pagamento_recorrente(
                    pagamento_response.orderID
                )
            raise exc

    def _enviar_email_agradecimento(self, campanha: Campanha, lead: Lead):
        foto_campanha = self._file_service.buscar_url_arquivo(campanha.capa)
        template = obrigado_pela_doacao_template(
            lead.nome, campanha.nome, foto_campanha
        )
        self._notification.enviar_email(
            lead.email, AssuntosEmailEnum.agradecimento_doacao, template
        )
