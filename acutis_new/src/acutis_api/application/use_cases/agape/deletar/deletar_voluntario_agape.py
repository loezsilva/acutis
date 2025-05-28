import uuid

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarVoluntarioAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(self, lead_id: uuid.UUID) -> None:
        nome_perfil_a_remover = PerfilEnum.voluntario_agape.value

        lead = self.agape_repository.buscar_lead_com_permissoes_por_id(lead_id)
        if not lead:
            raise HttpNotFoundError(f'Lead com ID {lead_id} não encontrado.')

        perfil_voluntario = self.agape_repository.buscar_perfil_por_nome(
            nome_perfil_a_remover
        )
        if not perfil_voluntario:
            raise HttpNotFoundError(
                f"Perfil '{nome_perfil_a_remover}' não encontrado no sistema."
            )

        permissao_removida = False
        for permissao in list(lead.permissoes_lead):
            if permissao.perfil_id == perfil_voluntario.id:
                self.agape_repository.remover_permissao_lead(permissao)
                permissao_removida = True
                break

        if not permissao_removida:
            raise HttpNotFoundError(
                f""""
                Lead com ID {lead_id} não possui o perfil
                '{nome_perfil_a_remover}' para ser removido.
                """
            )

        self.agape_repository.salvar_alteracoes()
