from acutis_api.communication.requests.vocacional import (
    ListarDesistenciaVocacionaisQuery,
)
from acutis_api.communication.responses.vocacional import (
    ListarDesistenciasVocacionaisResponse,
)
from acutis_api.communication.schemas.vocacional import (
    ListarDesistenciasVocacionaisSchema,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)


class ListarDesistenciasVocacionaisUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, filtros: ListarDesistenciaVocacionaisQuery):
        paginacao = (
            self.__vocacional_repository.buscar_desistencias_vocacionais(  # noqa: E501
                filtros
            )
        )

        lista_desistencias = [
            ListarDesistenciasVocacionaisSchema(
                usuario_vocacional_id=usuario_vocacional.id,
                nome=usuario_vocacional.nome,
                genero=usuario_vocacional.genero,
                email=usuario_vocacional.email,
                desistencia_em=(etapa.criado_em.strftime('%d/%m/%y %H:%M:%S')),
                etapa=etapa.etapa,
                pais=usuario_vocacional.pais,
                telefone=usuario_vocacional.telefone,
            )
            for usuario_vocacional, etapa in paginacao.items
        ]

        response = {
            'desistencias': lista_desistencias,
            'pagina': paginacao.page,
            'total': paginacao.total,
        }

        return ListarDesistenciasVocacionaisResponse.model_validate(response)
