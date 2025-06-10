import uuid

from acutis_api.communication.responses.admin_membros import (
    BuscarDoacoesECampanhasDoMembroResponse,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)


class BuscarDoacoesECampanhasDoMembroUseCase:
    def __init__(self, repository: AdminMembrosRepositoryInterface):
        self._repository = repository

    def execute(
        self, membro_id: uuid.UUID
    ) -> BuscarDoacoesECampanhasDoMembroResponse:
        resultado = self._repository.buscar_estatisticas_doacoes_do_membro(
            membro_id
        )
        numero_campanhas = (
            self._repository.buscar_numero_de_campanhas_do_membro(membro_id)
        )

        response = BuscarDoacoesECampanhasDoMembroResponse(
            num_doacoes=resultado.quantidade_doacoes,
            quantia_total_doada=round(resultado.valor_total_doacoes, 2),
            num_registros_em_campanhas=numero_campanhas,
            data_ultima_doacao=resultado.ultima_doacao,
        ).model_dump()

        return response
