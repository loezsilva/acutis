from uuid import UUID

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AdicionarVoluntarioAgapeUseCase:
    """
    Caso de uso para adicionar um voluntário
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self,
        lead_id: UUID,
    ) -> None:
        lead = self.__repository.buscar_lead_por_id(lead_id)
        if not lead:
            raise HttpNotFoundError('Usuário não encontrado.')

        perfil = self.__repository.buscar_perfil_por_nome(
            PerfilEnum.voluntario_agape.value
        )

        if not perfil:
            raise HttpNotFoundError('Perfil de voluntário não encontrado.')

        primeira_permissao_lead = (
            self.__repository.buscar_primeira_permissao_por_lead_id(lead_id)
        )

        primeira_permissao_lead.perfil_id = perfil.id

        self.__repository.salvar_alteracoes()
