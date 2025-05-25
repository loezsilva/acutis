import uuid

from werkzeug.datastructures import FileStorage

from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError


class FileService:
    def __init__(self, file_service: FileServiceInterface):
        self._service = file_service

    def buscar_url_arquivo(self, nome_arquivo: str) -> str:
        return self._service.buscar_url_arquivo(nome_arquivo)

    def salvar_arquivo(
        self,
        arquivo: FileStorage,
        nome_arquivo: str | None = None,
        extra_args: dict | None = None,
    ) -> str:
        if not nome_arquivo:
            if not arquivo.filename:
                raise HttpBadRequestError('Nome do arquivo inválido.')

            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            extensoes_permitidas = {'png', 'jpg', 'jpeg', '.xlsx'}
            if extensao not in extensoes_permitidas:
                raise HttpBadRequestError('Extensão do arquivo não permitida.')

            nome_arquivo = f'{str(uuid.uuid4())}.{extensao}'

        self._service.salvar_arquivo(arquivo, nome_arquivo, extra_args)
        return nome_arquivo
