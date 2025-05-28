from datetime import date, timedelta

from acutis_api.application.utils.funcoes_auxiliares import buscar_data_valida
from acutis_api.communication.responses.admin_benfeitores import (
    BuscarCardsBenfeitoresResponse,
    CardsBenfeitoresTotalPercentualSchema,
)
from acutis_api.domain.repositories.admin_benfeitores import (
    AdminBenfeitoresRepositoryInterface,
)


class BuscarCardsBenfeitoresUseCase:
    def __init__(self, repository: AdminBenfeitoresRepositoryInterface):
        self._repository = repository

    def execute(self):
        hoje = date.today()
        mes_atual_inicio = hoje.replace(day=1)
        mes_atual_final = hoje

        mes_anterior = mes_atual_inicio - timedelta(days=1)
        mes_anterior_inicio = mes_anterior.replace(day=1)

        mes_anterior_ano = mes_anterior.year
        mes_anterior_mes = mes_anterior.month
        mes_anterior_final = buscar_data_valida(
            hoje.day, mes_anterior_mes, mes_anterior_ano
        )
        cards_doacoes = self._repository.buscar_cards_doacoes_benfeitores(
            mes_atual_inicio=mes_atual_inicio,
            mes_atual_final=mes_atual_final,
            mes_anterior_inicio=mes_anterior_inicio,
            mes_anterior_final=mes_anterior_final,
        )

        response = BuscarCardsBenfeitoresResponse(
            benfeitores=CardsBenfeitoresTotalPercentualSchema(
                total=cards_doacoes.total_benfeitores,
                percentual=round(cards_doacoes.percentual_benfeitores, 2),
            ),
            doacoes_anonimas=CardsBenfeitoresTotalPercentualSchema(
                total=cards_doacoes.total_doacoes_anonimas,
                percentual=round(
                    cards_doacoes.percentual_quantidade_doacoes, 2
                ),
            ),
            montante=CardsBenfeitoresTotalPercentualSchema(
                total=round(cards_doacoes.total_montante_anonimo, 2),
                percentual=round(cards_doacoes.percentual_total_valor, 2),
            ),
            ticket_medio=CardsBenfeitoresTotalPercentualSchema(
                total=round(cards_doacoes.ticket_medio_anonimo, 2),
                percentual=round(cards_doacoes.percentual_ticket_medio, 2),
            ),
        ).model_dump()

        return response
