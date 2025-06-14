import math
import uuid

from flask import request

from acutis_api.communication.requests.agape import BeneficiariosCicloAcaoQuery
from acutis_api.communication.responses.agape import (
    FamiliaBeneficiariaResponse,
    ListarBeneficiariosAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarBeneficiariosAgapeUseCase:
    """
    Caso de uso para listar os beneficiários de um ciclo de ação ágape.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, ciclo_acao_id: uuid.UUID
    ) -> ListarBeneficiariosAgapeResponse:
        filtros: BeneficiariosCicloAcaoQuery = (
            BeneficiariosCicloAcaoQuery.parse_obj(request.args)
        )

        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            ciclo_acao_id
        )

        if ciclo_acao is None:
            raise HttpNotFoundError('Ciclo de ação não encontrado.')

        familias_beneficiadas = (
            self.agape_repository.listar_familias_beneficiadas_por_ciclo_id(
                ciclo_acao_id=ciclo_acao_id, filtros=filtros
            )
        )

        beneficiarios, total = self.agape_repository.query_paginada(
            familias_beneficiadas,
            filtros.pagina,
            filtros.por_pagina,
        )

        return ListarBeneficiariosAgapeResponse(
            total=total,
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            por_pagina=filtros.por_pagina,
            resultados=[
                FamiliaBeneficiariaResponse(
                    doacao_id=str(beneficiario[0]),
                    nome_familia=beneficiario[1],
                    data_hora_doacao=beneficiario[2],
                    recibos=beneficiario[3] if beneficiario[3] else [],
                ).model_dump()
                for beneficiario in beneficiarios
            ],
        ).model_dump()
