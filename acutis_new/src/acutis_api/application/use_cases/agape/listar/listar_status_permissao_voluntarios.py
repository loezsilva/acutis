from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.responses.agape import (
    ListarStatusPermissaoVoluntariosResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarStatusPermissaoVoluntariosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self,
    ) -> ListarStatusPermissaoVoluntariosResponse:
        perfil_voluntario = self.agape_repository.buscar_perfil_por_nome(
            PerfilEnum.voluntario_agape.value
        )
        if perfil_voluntario is None:
            raise HttpNotFoundError('Perfil de voluntário não encontrado.')

        permissao = self.agape_repository.buscar_permissoes_perfil(
            perfil_voluntario
        )

        if permissao is None:
            raise HttpNotFoundError('Permissão não encontrada.')

        return ListarStatusPermissaoVoluntariosResponse(
            acessar=permissao.acessar,
            criar=permissao.criar,
            editar=permissao.editar,
            deletar=permissao.deletar,
        ).model_dump()
