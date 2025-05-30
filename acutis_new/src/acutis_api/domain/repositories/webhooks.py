from abc import ABC, abstractmethod

from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.entities.processamento_doacao import ProcessamentoDoacao
from acutis_api.domain.repositories.schemas.webhooks import (
    BuscarDadosDoacaoSchema,
    RegistrarDoacaoAnonimaSchema,
)


class WebhooksRepositoryInterface(ABC):
    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def buscar_campanha_doacao_por_chave_pix(
        self, chave_pix: str
    ) -> CampanhaDoacao | None: ...

    @abstractmethod
    def buscar_benfeitor_por_numero_documento(
        self, numero_documento: str
    ) -> Benfeitor | None: ...

    @abstractmethod
    def registrar_benfeitor(
        self, nome: str, numero_documento: str
    ) -> Benfeitor: ...

    @abstractmethod
    def registrar_doacao_anonima(
        self,
        dados_doacao: RegistrarDoacaoAnonimaSchema,
    ): ...

    @abstractmethod
    def buscar_processamento_doacao_por_codigo_transacao(
        self, codigo_transacao: str
    ) -> ProcessamentoDoacao | None: ...

    @abstractmethod
    def atualizar_status_processamento_doacao(
        self,
        processamento_doacao: ProcessamentoDoacao,
        codigo_comprovante: str,
    ): ...

    @abstractmethod
    def buscar_dados_doacao_por_processamento_doacao(
        self,
        processamento_doacao: ProcessamentoDoacao,
    ) -> BuscarDadosDoacaoSchema: ...

    @abstractmethod
    def registrar_novo_processamento_doacao(
        self,
        pagamento_doacao_id: str,
        codigo_referencia: str,
        codigo_transacao: str,
        status_processamento: str,
    ) -> ProcessamentoDoacao: ...

    @abstractmethod
    def buscar_pagamento_doacao_por_codigo_ordem(
        self, codigo_ordem_pagamento: str
    ) -> PagamentoDoacao | None: ...
