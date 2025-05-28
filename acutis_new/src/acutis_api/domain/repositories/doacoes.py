import uuid
from abc import ABC, abstractmethod

from acutis_api.domain.entities import (
    Benfeitor,
    Campanha,
    Doacao,
    Lead,
    Membro,
    ProcessamentoDoacao,
)
from acutis_api.domain.repositories.schemas.doacoes import (
    RegistrarDoacaoSchema,
)


class DoacoesRepositoryInterface(ABC):
    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def buscar_campanha_por_id(self, id: uuid.UUID) -> Campanha | None: ...

    @abstractmethod
    def buscar_benfeitor_por_numero_documento(
        self, numero_documento: str
    ) -> Benfeitor | None: ...

    @abstractmethod
    def registrar_membro_benfeitor(
        self, membro: Membro, numero_documento: str, nome: str
    ) -> Benfeitor: ...

    @abstractmethod
    def vincular_membro_benfeitor(
        self, membro: Membro, benfeitor: Benfeitor
    ): ...

    @abstractmethod
    def registrar_doacao(self, dados_doacao: RegistrarDoacaoSchema): ...

    @abstractmethod
    def buscar_doacao_por_id(self, id: uuid.UUID) -> Doacao | None: ...

    @abstractmethod
    def cancelar_doacao_recorrente(self, doacao: Doacao, lead: Lead): ...

    @abstractmethod
    def buscar_processamento_doacao_por_id(
        self, id: uuid.UUID
    ) -> ProcessamentoDoacao | None: ...

    @abstractmethod
    def estornar_processamento_doacao_recorrente(
        self, processamento_doacao: ProcessamentoDoacao
    ): ...

    @abstractmethod
    def estornar_processamento_doacao_unica(
        self, processamento_doacao: ProcessamentoDoacao
    ): ...

    @abstractmethod
    def atualizar_doacao_pix_recorrente(
        self, processamento_doacao: ProcessamentoDoacao, codigo_transacao: str
    ): ...
