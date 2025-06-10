from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class AtualizarPermissoesVoluntariosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(self) -> None:
        perfil_voluntuntario_agape = (
            self.agape_repository.buscar_perfil_por_nome(
                nome_perfil=PerfilEnum.voluntario_agape.value
            )
        )

        permissao = self.agape_repository.buscar_permissoes_valuntarios(
            perfil_voluntario=perfil_voluntuntario_agape
        )

        if permissao:
            self.agape_repository.atualizar_permissoes_voluntario_agape(
                permissao=permissao
            )

        self.agape_repository.salvar_alteracoes()
