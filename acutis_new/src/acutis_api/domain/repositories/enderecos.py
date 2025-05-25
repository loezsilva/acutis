from abc import ABC, abstractmethod


class EnderecosRepositoryInterface(ABC):
    @abstractmethod
    def buscar_cep(self, cep: str) -> dict | None: ...
