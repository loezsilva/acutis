from acutis_api.communication.requests.membros import (
    AtualizarFotoMembroFormData,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros import (
    MembrosRepositoryInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AtualizarFotoMembroUseCase:
    def __init__(
        self,
        repository: MembrosRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._repository = repository
        self._file_service = file_service

    def execute(
        self, request: AtualizarFotoMembroFormData, usuario_logado: Lead
    ) -> ResponsePadraoSchema:
        if not request.foto:
            raise HttpNotFoundError('Nenhuma foto nova adicionada.')

        nova_foto = self._file_service.salvar_arquivo(request.foto)

        usuario_logado.membro.foto = nova_foto

        self._repository.salvar_alteracoes()

        return ResponsePadraoSchema(msg='Foto atualizada com sucesso.')
