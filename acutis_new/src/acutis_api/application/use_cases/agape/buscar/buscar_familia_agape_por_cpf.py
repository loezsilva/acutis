from uuid import UUID

from acutis_api.communication.responses.agape import (
    EnderecoResponse,
    FamiliaAgapeDetalhesPorCpfResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarFamiliaAgapePorCpfUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(
        self, cpf: str, ciclo_acao_id: UUID
    ) -> FamiliaAgapeDetalhesPorCpfResponse:
        cpf_a_buscar = cpf

        membro = self._agape_repository.buscar_membro_por_cpf(cpf_a_buscar)
        if not membro:
            raise HttpNotFoundError(
                'Nenhum membro encontrado com o CPF fornecido.'
            )
        if not membro.fk_familia_agape_id:
            raise HttpNotFoundError(
                f"""Membro com CPF {cpf_a_buscar} não está
                  associado a nenhuma família."""
            )

        familia = self._agape_repository.buscar_familia_por_id(
            membro.fk_familia_agape_id
        )
        if not familia:
            raise HttpNotFoundError(f"""
            Família com ID {membro.fk_familia_agape_id}
              não encontrada ou está inativa.
            """)

        endereco_response_data = None
        if familia.fk_endereco_id:
            endereco_entity = self._agape_repository.buscar_endereco_por_id(
                familia.fk_endereco_id
            )
            if endereco_entity:
                endereco_response_data = EnderecoResponse.model_validate(
                    endereco_entity
                )

        fotos_entities = self._agape_repository.listar_fotos_por_familia_id(
            familia.id
        )
        fotos_urls = [
            self._file_service.buscar_url_arquivo(foto.foto)
            for foto in fotos_entities
            if foto.foto
        ]

        ultimo_recebimento_data = (
            self._agape_repository.buscar_ultimo_recebimento_familia_no_ciclo(
                familia_id=familia.id, ciclo_acao_id=ciclo_acao_id
            )
        )

        comprovante_url = None
        if familia.comprovante_residencia:
            comprovante_url = self._file_service.buscar_url_arquivo(
                familia.comprovante_residencia
            )

        return FamiliaAgapeDetalhesPorCpfResponse(
            id=familia.id,
            nome_familia=familia.nome_familia,
            observacao=familia.observacao,
            comprovante_residencia_url=comprovante_url,
            criado_em=familia.criado_em,
            ativo=familia.deletado_em is None,
            ultimo_recebimento=(
                ultimo_recebimento_data if ultimo_recebimento_data else None
            ),
            endereco=endereco_response_data,
            fotos_familia_urls=fotos_urls,
        )
