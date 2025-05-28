from abc import ABC, abstractmethod

from acutis_api.domain.services.schemas.gateway_pagamento import (
    BuscarPagamentoPixResponse,
    CriarPagamentoBolecodeRequest,
    CriarPagamentoPixSchema,
)


class GatewayPagamentoInterface(ABC):
    @abstractmethod
    def criar_pagamento_pix(
        self, pagamento: CriarPagamentoPixSchema
    ) -> BuscarPagamentoPixResponse: ...

    @abstractmethod
    def buscar_pagamento_pix(
        self, transacao_id: str
    ) -> BuscarPagamentoPixResponse: ...

    @abstractmethod
    def criar_pagamento_bolecode(
        self, dados_pagamento: CriarPagamentoBolecodeRequest
    ): ...

    @abstractmethod
    def registrar_chave_pix_webhook(self, chave_pix: str) -> None: ...

    @abstractmethod
    def deletar_chave_pix_webhook(self, chave_pix: str): ...
