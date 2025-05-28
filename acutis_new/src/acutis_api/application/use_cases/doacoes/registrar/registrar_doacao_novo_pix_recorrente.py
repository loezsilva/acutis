from datetime import datetime

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    calcular_data_vencimento,
    definir_tipo_documento,
    verificar_token,
)
from acutis_api.communication.requests.doacoes import (
    PagamentoPixRecorrenteTokenQuery,
)
from acutis_api.communication.responses.doacoes import (
    RegistrarDoacaoPixResponse,
)
from acutis_api.communication.schemas.doacoes import PixRecorrenteTokenSchema
from acutis_api.domain.entities.processamento_doacao import ProcessamentoDoacao
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.domain.services.schemas.gateway_pagamento import (
    BuscarPagamentoPixResponse,
    CriarPagamentoPixSchema,
)
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class RegistrarDoacaoNovoPixRecorrenteUseCase:
    def __init__(
        self,
        repository: DoacoesRepositoryInterface,
        itau: GatewayPagamentoInterface,
    ):
        self._repository = repository
        self._itau = itau

    def execute(self, query: PagamentoPixRecorrenteTokenQuery):
        data_expiracao_token = 24 * 60 * 60 * 7

        payload = PixRecorrenteTokenSchema.model_validate(
            verificar_token(
                token=query.token,
                salt=TokenSaltEnum.gerar_novo_pagamento_recorrencia_pix.value,
                max_age=data_expiracao_token,
            )
        )

        processamento_doacao = (
            self._repository.buscar_processamento_doacao_por_id(
                payload.processamento_doacao_id
            )
        )

        data_vencimento = calcular_data_vencimento(
            processamento_doacao.criado_em.date()
        )

        if processamento_doacao.codigo_transacao:
            response = self._itau.buscar_pagamento_pix(
                processamento_doacao.codigo_transacao
            )
        else:
            response = self._gerar_pagamento_pix(
                payload, processamento_doacao, data_vencimento
            )

        return RegistrarDoacaoPixResponse(
            pix_copia_cola=response.pix_copia_cola,
            qrcode=response.qrcode,
            data_vencimento=data_vencimento,
        ).model_dump()

    def _gerar_pagamento_pix(
        self,
        payload: PixRecorrenteTokenSchema,
        processamento_doacao: ProcessamentoDoacao,
        data_vencimento: str,
    ) -> BuscarPagamentoPixResponse:
        tipo_documento = definir_tipo_documento(payload.numero_documento)

        if (
            datetime.strptime(data_vencimento, '%Y-%m-%d').date()
            < datetime.today().date()
        ):
            raise HttpUnprocessableEntityError(
                'Esse pagamento não está mais disponível.'
            )

        dados_pagamento = CriarPagamentoPixSchema(
            data_vencimento=data_vencimento,
            tipo_documento=tipo_documento,
            numero_documento=payload.numero_documento,
            nome=payload.nome,
            valor_doacao=processamento_doacao.pagamento_doacao.valor,
            chave_pix=payload.chave_pix,
        )

        response = self._itau.criar_pagamento_pix(dados_pagamento)

        self._repository.atualizar_doacao_pix_recorrente(
            processamento_doacao, response.transacao_id
        )
        self._repository.salvar_alteracoes()

        return response
