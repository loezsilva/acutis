from acutis_api.communication.requests.vocacional import (
    ListarVocacionaisRecusadosQuery,
)
from acutis_api.communication.responses.vocacional import (
    ListarVocacionaisRecusadosResponse,
)
from acutis_api.communication.schemas.vocacional import (
    ListarVocacionaisRecusadosSchema,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)


class ListarVocacionaisRecusadosUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, filtros: ListarVocacionaisRecusadosQuery):
        paginacao = self.__vocacional_repository.buscar_vocacionais_recusados(
            filtros
        )

        recusados = [
            ListarVocacionaisRecusadosSchema(
                justificativa=etapa.justificativa,
                usuario_vocacional_id=usuario_vocacional.id,
                nome=usuario_vocacional.nome,
                genero=usuario_vocacional.genero,
                email=usuario_vocacional.email,
                telefone=usuario_vocacional.telefone,
                reprovado_em=etapa.criado_em.strftime('%d/%m/%y %H:%M:%S'),
                etapa=etapa.etapa,
                pais=usuario_vocacional.pais,
                responsavel=(
                    f'{
                        self.__vocacional_repository.busca_responsavel_atualizou_status(
                            etapa.fk_responsavel_id, etapa.etapa
                        )
                    } - {etapa.criado_em.strftime("%d/%m/%Y %H:%M:%S")}'
                    if etapa.fk_responsavel_id is not None
                    else None
                ),
            )
            for usuario_vocacional, etapa in paginacao.items
        ]

        response = {
            'recusados': recusados,
            'pagina': paginacao.page,
            'total': paginacao.total,
        }

        return ListarVocacionaisRecusadosResponse.model_validate(response)
