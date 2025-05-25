from acutis_api.communication.responses.admin_graficos_cadastros import (
    QuantidadeCadastrosMesAtualResponse,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class QuantidadeCadastrosUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self):
        quantidade_mes_atual = self.__repository.quantidade_membros_mes_atual()
        media_mensal = self.__repository.media_mensal_membros()

        calculo_porcentagem = (
            (quantidade_mes_atual - media_mensal) / media_mensal
        ) * 100

        return QuantidadeCadastrosMesAtualResponse(
            porcentagem=round(calculo_porcentagem, 2),
            quantidade_cadastro_mes_atual=quantidade_mes_atual,
        )
