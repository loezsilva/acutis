from acutis_api.communication.responses.agape import ItemEstoqueAgapeResponse
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


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
        # Busca o item de estoque pelo ID
        self.__repository.adicionar_voluntario_agape(lead_id)

        # Persiste as alterações
        self.__repository.salvar_alteracoes()

        return 
