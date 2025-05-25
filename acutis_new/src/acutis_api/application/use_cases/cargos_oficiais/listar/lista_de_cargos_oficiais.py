from acutis_api.communication.responses.cargos_oficiais import (
    ListaDeCargosOficiaisSchema,
)
from acutis_api.domain.repositories.cargos_oficiais import (
    CargosOficiaisRepositoryInterface,
)


class ListaDeCargosOficiaisUseCase:
    def __init__(self, repository: CargosOficiaisRepositoryInterface):
        self.repository = repository

    def execute(self):
        cargos_oficiais = self.repository.lista_de_cargos_oficiais()

        return [
            ListaDeCargosOficiaisSchema(
                id=cargos_oficiais.id,
                nome_cargo=cargos_oficiais.nome_cargo,
            ).model_dump()
            for cargos_oficiais in cargos_oficiais
        ]
