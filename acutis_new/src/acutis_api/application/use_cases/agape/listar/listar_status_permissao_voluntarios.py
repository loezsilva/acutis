import math
from typing import List, Set

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.responses.agape import (
    ListarStatusPermissaoVoluntariosResponse,
    StatusPermissaoVoluntario,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import PaginacaoSchema


class ListarStatusPermissaoVoluntariosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, filtros_api: PaginacaoSchema
    ) -> ListarStatusPermissaoVoluntariosResponse:
        nomes_perfis_agape: Set[str] = {
            PerfilEnum.voluntario_agape.value,
            PerfilEnum.administrador_agape.value,
        }

        filtros_repo = PaginacaoSchema(
            pagina=filtros_api.pagina, por_pagina=filtros_api.por_pagina
        )

        leads, total = self.agape_repository.listar_leads_por_nomes_de_perfis(
            nomes_perfis=list(nomes_perfis_agape),
            filtros_paginacao=filtros_repo,
        )

        resultados: List[StatusPermissaoVoluntario] = []
        for lead_ent in leads:
            perfis_do_lead_filtrados = []
            if lead_ent.permissoes_lead:
                for p in lead_ent.permissoes_lead:
                    if p.perfil and p.perfil.nome in nomes_perfis_agape:
                        perfis_do_lead_filtrados.append(p.perfil.nome)

            resultados.append(
                StatusPermissaoVoluntario(
                    lead_id=lead_ent.id,
                    nome=lead_ent.nome,
                    email=lead_ent.email,
                    perfis_agape=sorted(list(set(perfis_do_lead_filtrados))),
                )
            )

        return ListarStatusPermissaoVoluntariosResponse(
            pagina=filtros_api.pagina,
            paginas=math.ceil(total / filtros_api.por_pagina),
            total=total,
            resultados=resultados,
        )
