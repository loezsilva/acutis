from abc import ABC, abstractmethod

from acutis_api.domain.entities.lead import Lead


class AutenticacaoRepositoryInterface(ABC):
    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def buscar_lead_por_email(self, email: str) -> Lead | None: ...

    @abstractmethod
    def atualizar_data_ultimo_acesso(self, lead: Lead): ...

    @abstractmethod
    def alterar_senha(usuario: Lead, nova_senha: str): ...
