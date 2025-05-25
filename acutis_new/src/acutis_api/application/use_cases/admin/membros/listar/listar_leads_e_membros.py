import math

from acutis_api.communication.requests.admin_membros import (
    ListarLeadsMembrosQuery,
)
from acutis_api.communication.responses.admin_membros import (
    LeadsMembrosSchema,
    ListarLeadsMembrosResponse,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface


class ListarLeadsMembrosUseCase:
    def __init__(
        self,
        repository: AdminMembrosRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._repository = repository
        self._file_service = file_service

    def execute(self, filtros: ListarLeadsMembrosQuery):
        leads_membros, total = self._repository.listar_leads_e_membros(filtros)

        response = ListarLeadsMembrosResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            leads_e_membros=[
                LeadsMembrosSchema(
                    lead_id=lead_membro.lead_id,
                    nome=lead_membro.nome,
                    email=lead_membro.email,
                    telefone=lead_membro.telefone,
                    pais=lead_membro.pais,
                    data_cadastro_lead=lead_membro.data_cadastro_lead,
                    lead_atualizado_em=lead_membro.lead_atualizado_em,
                    membro_id=lead_membro.membro_id,
                    benfeitor_id=lead_membro.benfeitor_id,
                    endereco_id=lead_membro.endereco_id,
                    nome_social=lead_membro.nome_social,
                    data_nascimento=lead_membro.data_nascimento,
                    numero_documento=lead_membro.numero_documento,
                    sexo=lead_membro.sexo,
                    foto=(
                        self._file_service.buscar_url_arquivo(lead_membro.foto)
                        if lead_membro.foto
                        else None
                    ),
                    ultimo_acesso=lead_membro.ultimo_acesso,
                    status_conta_lead=lead_membro.status_conta_lead,
                    data_cadastro_membro=lead_membro.data_cadastro_membro,
                    membro_atualizado_em=lead_membro.membro_atualizado_em,
                    cadastro_membro_atualizado_em=(
                        lead_membro.cadastro_membro_atualizado_em
                    ),
                )
                for lead_membro in leads_membros
            ],
        )

        return response
