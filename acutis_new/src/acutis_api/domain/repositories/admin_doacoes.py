import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.repositories.schemas.admin_doacoes import (
    ListarDoacoesQuery,
    ListarDoacoesSchema,
)


class AdminDoacoesRepositoryInterface(ABC):
    @abstractmethod
    def listar_doacoes(
        self, filtros: ListarDoacoesQuery
    ) -> tuple[list[ListarDoacoesSchema], int]: ...

    @abstractmethod
    def busca_doacao_por_id(self, fk_doacao_id: uuid.UUID): ...

    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def alterar_considerar_doacao(self, doacao: Doacao): ...

    @abstractmethod
    def contabilizar_recorrencia_nao_efetuada_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> tuple[int, float]: ...

    @abstractmethod
    def contabilizar_recorrencia_total(self) -> tuple[int, float, int]: ...

    @abstractmethod
    def contabilizar_recorrencia_prevista_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> tuple[int, float]: ...

    @abstractmethod
    def contabilizar_lembretes_efetivos(self) -> tuple[int, float]: ...

    @abstractmethod
    def contabilizar_recorrencias_efetuadas_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> tuple[int, float]: ...

    @abstractmethod
    def contabilizar_recorrencias_canceladas(self) -> tuple[int, float]: ...
