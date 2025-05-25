from datetime import datetime

from acutis_api.application.utils.funcoes_auxiliares import (
    quantidade_dias_entre_datas,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class MembrosMediaDiariaUseCase:
    def __init__(self, respository: GraficosCadastrosRepositoryInterface):
        self.__repository = respository

    def execute(self) -> int:
        data_primeiro_membro, quantidade_membro_total = (
            self.__repository.media_diaria_membros()
        )

        quantidade_dias = quantidade_dias_entre_datas(
            data_primeiro_membro, datetime.now()
        )

        media_diaria = quantidade_membro_total / quantidade_dias

        return int(media_diaria)
