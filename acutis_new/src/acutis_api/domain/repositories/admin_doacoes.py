import uuid
from abc import ABC, abstractmethod

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
