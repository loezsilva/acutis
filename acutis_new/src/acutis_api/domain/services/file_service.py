from abc import ABC, abstractmethod

from werkzeug.datastructures import FileStorage


class FileServiceInterface(ABC):
    @abstractmethod
    def buscar_url_arquivo(self, nome_arquivo: str) -> str: ...

    @abstractmethod
    def salvar_arquivo(
        self,
        arquivo: FileStorage,
        nome_arquivo: str,
        extra_args: dict | None = None,
    ) -> str: ...
