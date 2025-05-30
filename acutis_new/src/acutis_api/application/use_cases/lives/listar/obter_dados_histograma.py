from typing import List

from acutis_api.communication.requests.lives import ObterHistogramaLiveRequest
from acutis_api.communication.responses.lives import (
    HistogramaLiveItem,
    LiveDataItem,
    ObterHistogramaLiveResponse,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ObterHistogramaLiveUseCase:
    def __init__(self, repository: LivesRepositoryInterface):
        self.repository = repository

    def execute(self, request: ObterHistogramaLiveRequest) -> List[dict]:
        resultado = self.repository.obter_dados_histograma(request)
        dados_agrupados = resultado['dados_agrupados']
        redes_sociais = resultado['redes_sociais']

        data = {}
        audiencias = []
        for row in dados_agrupados:
            titulo = row.titulo
            audiencia_total = row.audiencia_total
            data_hora = f'{row.data} {int(row.hora):02}:{int(row.minuto):02}'
            audiencias.append(audiencia_total)

            if titulo not in data:
                data[titulo] = []

            data[titulo].append(
                HistogramaLiveItem(
                    horario=data_hora, audiencia=audiencia_total
                )
            )

        if not audiencias:
            raise HttpNotFoundError(
                'Nenhum histograma encontrado para a live.'
            )

        total_geral = sum(rs.total_audiencia for rs in redes_sociais)
        canal_principal = max(redes_sociais, key=lambda rs: rs.total_audiencia)
        canal_principal_nome = canal_principal.rede_social
        canal_principal_porcentagem = (
            canal_principal.total_audiencia / total_geral
        ) * 100

        response = ObterHistogramaLiveResponse(
            audiencia_maxima=max(audiencias),
            audiencia_minima=min(audiencias),
            audiencia_media=round(sum(audiencias) / len(audiencias)),
            canal_principal=f'{canal_principal_nome} - {
                canal_principal_porcentagem:.2f
            }%',
            live_data=[
                LiveDataItem(titulo=titulo, dados=dados)
                for titulo, dados in data.items()
            ],
        ).model_dump()

        return response
