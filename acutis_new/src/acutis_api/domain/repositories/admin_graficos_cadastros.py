from abc import ABC, abstractmethod

from acutis_api.domain.entities.lead import Lead


class GraficosCadastrosRepositoryInterface(ABC):
    @abstractmethod
    def quantidade_leads_mes_atual(self) -> int: ...

    @abstractmethod
    def media_mensal_leads(self) -> int: ...

    @abstractmethod
    def quantidade_membros_mes_atual(self) -> int: ...

    @abstractmethod
    def quantidade_membros_dia_atual(self) -> int: ...

    @abstractmethod
    def quantidade_membros_por_genero(self) -> list: ...

    @abstractmethod
    def quantidade_leads_por_hora(self) -> list: ...

    @abstractmethod
    def quantidade_membros_por_dia_mes_atual(self) -> list: ...

    @abstractmethod
    def quantidade_membros_por_hora_dia_atual(self) -> list: ...

    @abstractmethod
    def leads_por_origem(self): ...

    @abstractmethod
    def leads_por_dia_semana(self) -> Lead: ...

    @abstractmethod
    def leads_por_origem_mes_atual(self) -> list: ...

    @abstractmethod
    def quantidade_leads_por_mes(self) -> list: ...

    @abstractmethod
    def quantidade_leads_total(self) -> int: ...

    @abstractmethod
    def quantidade_membros_por_idade(self) -> list: ...

    @abstractmethod
    def leads_por_evolucao_mensal(self) -> list: ...
