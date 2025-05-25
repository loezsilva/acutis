import uuid
from abc import ABC

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
    def salvar_alteracoes(self): ...

    def buscar_campanha_por_id(self, id: uuid.UUID) -> Campanha | None: ...

    def buscar_benfeitor_por_numero_documento(
        self, numero_documento: str
    ) -> Benfeitor | None: ...

    def registrar_membro_benfeitor(
        self, membro: Membro, numero_documento: str, nome: str
    ) -> Benfeitor: ...

    def vincular_membro_benfeitor(
        self, membro: Membro, benfeitor: Benfeitor
    ): ...

    def registrar_doacao(self, dados_doacao: RegistrarDoacaoSchema): ...

    def buscar_doacao_por_id(self, id: uuid.UUID) -> Doacao | None: ...

    def cancelar_doacao_recorrente(self, doacao: Doacao, lead: Lead): ...

    def buscar_processamento_doacao_por_id(
        self, id: uuid.UUID
    ) -> ProcessamentoDoacao | None: ...

    def estornar_processamento_doacao_recorrente(
        self, processamento_doacao: ProcessamentoDoacao
    ): ...

    def estornar_processamento_doacao_unica(
        self, processamento_doacao: ProcessamentoDoacao
    ): ...
