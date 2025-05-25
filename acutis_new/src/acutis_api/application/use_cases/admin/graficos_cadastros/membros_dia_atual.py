from datetime import datetime

from acutis_api.application.utils.funcoes_auxiliares import (
    quantidade_dias_entre_datas,
)
from acutis_api.communication.responses.admin_graficos_cadastros import (
    QuantidadeCadastrosDiaAtualResponse,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class QuantidadeCadastrosDiaAtualUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> QuantidadeCadastrosDiaAtualResponse:
        quantidade_dia_atual = self.__repository.quantidade_membros_dia_atual()
        data_primeiro_membro, quantidade_membro_total = (
            self.__repository.media_diaria_membros()
        )

        quantidade_dias = quantidade_dias_entre_datas(
            data_primeiro_membro, datetime.now()
        )

        media_diaria = quantidade_membro_total / quantidade_dias

        calculo_porcentagem = (
            (quantidade_dia_atual - media_diaria) / media_diaria
        ) * 100

        return QuantidadeCadastrosDiaAtualResponse(
            quantidade_cadastro_dia_atual=quantidade_dia_atual,
            porcentagem=round(calculo_porcentagem, 2),
        )
