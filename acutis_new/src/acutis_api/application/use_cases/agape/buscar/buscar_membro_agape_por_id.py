from uuid import UUID

from acutis_api.communication.responses.agape import (
    MembroAgapeDetalhesResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarMembroAgapePorIdUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(self, membro_agape_id: UUID) -> MembroAgapeDetalhesResponse:
        membro = self._agape_repository.buscar_membro_agape_por_id(
            membro_agape_id
        )
        if not membro:
            # Para consistência com outros métodos de
            # busca por ID que levantam erro no repo.
            raise HttpNotFoundError(
                f'Membro Ágape com ID {membro_agape_id} não encontrado.'
            )

        foto_documento_url = None
        if membro.foto_documento:
            foto_documento_url = self._file_service.get_public_url(
                membro.foto_documento
            )

        return MembroAgapeDetalhesResponse(
            id=membro.id,
            familia_agape_id=membro.fk_familia_agape_id,
            nome=membro.nome,
            email=membro.email,
            telefone=membro.telefone,
            cpf=membro.cpf,
            data_nascimento=membro.data_nascimento,  # Deve ser 'date'
            responsavel=membro.responsavel,
            funcao_familiar=membro.funcao_familiar,
            escolaridade=membro.escolaridade,
            ocupacao=membro.ocupacao,
            renda=membro.renda,
            foto_documento_url=foto_documento_url,
            beneficiario_assistencial=membro.beneficiario_assistencial,
            criado_em=membro.criado_em,  # Vem de ModeloBase
            atualizado_em=membro.atualizado_em,  # Vem de ModeloBase
        )
