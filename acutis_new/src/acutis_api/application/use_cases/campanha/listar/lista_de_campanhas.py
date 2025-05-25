from acutis_api.communication.responses.campanha import ListaDeCampanhasSchema
from acutis_api.domain.repositories.campanha import (
    CampanhaRepositoryInterface,
)


class ListaDeCampanhasUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self.repository = repository

    def execute(self):
        campanhas = self.repository.lista_de_campanhas()

        return [
            ListaDeCampanhasSchema(
                id=campanha.id,
                nome_campanha=campanha.nome,
            ).model_dump()
            for campanha in campanhas
        ]
