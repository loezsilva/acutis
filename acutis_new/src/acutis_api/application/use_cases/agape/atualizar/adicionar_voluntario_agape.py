from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.domain.entities.perfil import Perfil
from acutis_api.communication.enums.membros import PerfilEnum

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
        lead_id,
    ) -> dict:
        
        lead = self.__repository.buscar_lead_por_id(lead_id)
        if not lead:
            raise HttpNotFoundError("Usuário não encontrado.")
        
        perfil = self.__repository.buscar_perfil_por_nome(
            PerfilEnum.voluntario_agape.value
        )

        if not perfil:
            raise HttpNotFoundError("Perfil de voluntário não encontrado.")
        
        permissoes = self.__repository.buscar_permissoes_por_lead_id(lead_id)

        primeira_permissao = permissoes.first()

        primeira_permissao.perfil_id = perfil.id
        
        self.__repository.adicionar_voluntario_agape(lead_id)

        self.__repository.salvar_alteracoes()

        return