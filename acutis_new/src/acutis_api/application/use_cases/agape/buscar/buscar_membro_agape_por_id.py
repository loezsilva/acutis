from uuid import UUID
from datetime import date, datetime # Adicionado date e datetime

from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import MembroAgapeDetalhesResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError # Já deve estar sendo levantado pelo repo
from acutis_api.domain.services.file_service import FileServiceInterface
# from acutis_api.domain.entities.membro_agape import MembroAgape # Entidade não precisa ser usada diretamente aqui

class BuscarMembroAgapePorIdUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface, file_service: FileServiceInterface):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(self, membro_agape_id: UUID) -> MembroAgapeDetalhesResponse:
        membro_entity = self._agape_repository.buscar_membro_agape_por_id(membro_agape_id)
        # O repositório já levanta HttpNotFoundError se não encontrar o membro.
        # Não é necessário checar 'deletado_em' aqui pois MembroAgape não tem esse campo em sua base.

        foto_documento_url = None
        if membro_entity.foto_documento:
            foto_documento_url = self._file_service.get_public_url(membro_entity.foto_documento)

        return MembroAgapeDetalhesResponse(
            id=membro_entity.id,
            fk_familia_agape_id=membro_entity.fk_familia_agape_id,
            nome=membro_entity.nome,
            email=membro_entity.email,
            telefone=membro_entity.telefone,
            cpf=membro_entity.cpf,
            data_nascimento=membro_entity.data_nascimento, # Deve ser 'date'
            responsavel=membro_entity.responsavel,
            funcao_familiar=membro_entity.funcao_familiar,
            escolaridade=membro_entity.escolaridade,
            ocupacao=membro_entity.ocupacao,
            renda=membro_entity.renda,
            foto_documento_url=foto_documento_url,
            beneficiario_assistencial=membro_entity.beneficiario_assistencial,
            criado_em=membro_entity.criado_em, # Vem de ModeloBase
            atualizado_em=membro_entity.atualizado_em # Vem de ModeloBase
        )
