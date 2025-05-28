from typing import List, Set

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.requests.agape import (
    AtualizarPermissoesVoluntariosRequestSchema,
)
from acutis_api.communication.responses.agape import (
    AtualizacaoPermissaoStatus,
    AtualizarPermissoesVoluntariosResponse,
)
from acutis_api.domain.entities.perfil import Perfil
from acutis_api.domain.entities.permissao_lead import PermissaoLead
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class AtualizarPermissoesVoluntariosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, request_data: AtualizarPermissoesVoluntariosRequestSchema
    ) -> AtualizarPermissoesVoluntariosResponse:
        resultados_finais: List[AtualizacaoPermissaoStatus] = []

        perfis_agape_gerenciaveis: Set[str] = {
            PerfilEnum.voluntario_agape.value,
            PerfilEnum.administrador_agape.value,
        }

        for atualizacao_info in request_data.atualizacoes:
            lead_id = atualizacao_info.lead_id
            perfis_solicitados_nomes: Set[str] = set(
                atualizacao_info.perfis_agape
            )

            lead = self.agape_repository.buscar_lead_com_permissoes_por_id(
                lead_id
            )

            if not lead:
                resultados_finais.append(
                    AtualizacaoPermissaoStatus(
                        lead_id=lead_id,
                        status=f'Erro: Lead com ID {lead_id} não encontrado.',
                    )
                )
                continue

            # Validar se todos os perfis solicitados existem no sistema
            perfis_solicitados_entidades: List[Perfil] = []
            todos_perfis_solicitados_validos = True
            for nome_perfil_solicitado in perfis_solicitados_nomes:
                perfil_ent = self.agape_repository.buscar_perfil_por_nome(
                    nome_perfil_solicitado
                )
                if not perfil_ent:
                    resultados_finais.append(
                        AtualizacaoPermissaoStatus(
                            lead_id=lead_id,
                            status=f"""
                            Erro: Perfil '{nome_perfil_solicitado}'
                            não encontrado no sistema.
                            """,
                            perfis_concedidos=[],
                        )
                    )
                    todos_perfis_solicitados_validos = False
                    break
                perfis_solicitados_entidades.append(perfil_ent)

            if not todos_perfis_solicitados_validos:
                continue  # Pula para o próximo lead_id

            perfis_validos_a_adicionar_entidades: List[Perfil] = [
                p_ent
                for p_ent in perfis_solicitados_entidades
                if p_ent.nome in perfis_agape_gerenciaveis
            ]

            permissoes_a_remover: List[PermissaoLead] = []
            for p_lead in list(lead.permissoes_lead):
                if (
                    p_lead.perfil
                    and p_lead.perfil.nome in perfis_agape_gerenciaveis
                ):
                    permissoes_a_remover.append(p_lead)

            for p_removida in permissoes_a_remover:
                self.agape_repository.remover_permissao_lead(p_removida)
                if p_removida in lead.permissoes_lead:
                    lead.permissoes_lead.remove(p_removida)

            perfis_concedidos_nomes: List[str] = []
            for perfil_para_adicionar in perfis_validos_a_adicionar_entidades:
                existe = any(
                    p_lead.perfil_id == perfil_para_adicionar.id
                    for p_lead in lead.permissoes_lead
                )
                if not existe:
                    nova_permissao = (
                        self.agape_repository.adicionar_permissao_lead(
                            lead_id=lead.id, perfil_id=perfil_para_adicionar.id
                        )
                    )
                    lead.permissoes_lead.append(nova_permissao)
                perfis_concedidos_nomes.append(perfil_para_adicionar.nome)

            resultados_finais.append(
                AtualizacaoPermissaoStatus(
                    lead_id=lead_id,
                    status='Atualizado com sucesso.',
                    perfis_concedidos=sorted(
                        list(set(perfis_concedidos_nomes))
                    ),
                )
            )

        if request_data.atualizacoes:
            self.agape_repository.salvar_alteracoes()

        return AtualizarPermissoesVoluntariosResponse(
            resultados=resultados_finais
        )
