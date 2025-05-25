from datetime import datetime

from acutis_api.application.use_cases.doacoes.registrar import (
    BaseRegistrarDoacaoUseCase,
)
from acutis_api.application.utils.funcoes_auxiliares import (
    calcular_data_vencimento,
    definir_tipo_documento,
)
from acutis_api.communication.requests.doacoes import (
    RegistrarDoacaoPixRequest,
)
from acutis_api.communication.responses.doacoes import (
    RegistrarDoacaoPixResponse,
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
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.domain.services.schemas.gateway_pagamento import (
    CriarPagamentoPixRequest,
)
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class RegistrarDoacaoPixUseCase(BaseRegistrarDoacaoUseCase):
    def __init__(
        self,
        repository: DoacoesRepositoryInterface,
        itau: GatewayPagamentoInterface,
        file_service: FileServiceInterface,
    ):
        super().__init__(repository)
        self._repository = repository
        self._itau = itau
        self._file_service = file_service

    def execute(self, request: RegistrarDoacaoPixRequest, lead: Lead):
        self._validar_lead(lead)
        campanha = self._buscar_campanha(request.campanha_id)
        self._vincular_ou_registrar_benfeitor(lead)

        response = self._realizar_doacao(request, campanha, lead)
        self._repository.salvar_alteracoes()

        return response

    def _realizar_doacao(
        self,
        request: RegistrarDoacaoPixRequest,
        campanha: Campanha,
        lead: Lead,
    ) -> RegistrarDoacaoPixResponse:
        data_atual = datetime.today().date()
        data_vencimento = calcular_data_vencimento(data_atual)

        tipo_documento = definir_tipo_documento(lead.membro.numero_documento)
        if tipo_documento == 'identidade_estrangeira':
            raise HttpUnprocessableEntityError(
                'Você precisa ter um CPF ou CNPJ cadastrado para doar por este meio de pagamento.'  # noqa
            )

        dados_pagamento = CriarPagamentoPixRequest(
            data_vencimento=data_vencimento,
            tipo_documento=tipo_documento,
            numero_documento=lead.membro.numero_documento,
            nome=lead.nome,
            valor_doacao=request.valor_doacao,
            chave_pix=campanha.campanha_doacao.chave_pix,
        )

        pix_response = self._itau.criar_pagamento_pix(dados_pagamento)

        dados_doacao = RegistrarDoacaoSchema(
            benfeitor_id=lead.membro.benfeitor.id,
            campanha_doacao_id=campanha.campanha_doacao.id,
            valor_doacao=request.valor_doacao,
            recorrente=request.recorrente,
            forma_pagamento=FormaPagamentoEnum.pix,
            anonimo=False,
            gateway=GatewayPagamentoEnum.itau,
            codigo_transacao=pix_response.transacao_id,
            status=StatusProcessamentoEnum.pendente,
        )
        self._repository.registrar_doacao(dados_doacao)

        return RegistrarDoacaoPixResponse(
            pix_copia_cola=pix_response.pix_copia_cola,
            qrcode=pix_response.qrcode,
            data_vencimento=data_vencimento,
        ).model_dump()
