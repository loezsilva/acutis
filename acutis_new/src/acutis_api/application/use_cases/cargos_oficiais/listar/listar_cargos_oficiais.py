from acutis_api.communication.requests.cargos_oficiais import (
    ListarCargosOficiaisQuery,
    ListarCargosOficiaisResponse,
    ListarCargosOficiaisSchema,
)
from acutis_api.domain.repositories.cargos_oficiais import (
    CargosOficiaisRepositoryInterface,
)


class ListarTodosCargosOficiaisUseCase:
    def __init__(self, repository: CargosOficiaisRepositoryInterface):
        self.__repository = repository

    def execute(
        self, filtros_request: ListarCargosOficiaisQuery
    ) -> ListarCargosOficiaisResponse:
        listagem = self.__repository.listar_todos_cargos_oficiais(
            filtros_request
        )

        response_cargos = (
            [
                ListarCargosOficiaisSchema(
                    id=cargo.id,
                    nome_cargo=cargo.nome_cargo,
                    criado_em=cargo.criado_em.strftime('%d/%m/%Y %H:%M:%S'),
                    criado_por=cargo.criado_por,
                    cargo_superior=(
                        self.__repository.busca_cargo_oficial_por_id(
                            cargo.fk_cargo_superior_id
                        ).nome_cargo
                        if (cargo.fk_cargo_superior_id is not None)
                        else None
                    ),
                )
                for cargo in listagem.items
            ]
            if listagem.items is not None
            else []
        )

        return ListarCargosOficiaisResponse(
            cargos=response_cargos,
            pagina=listagem.page,
            paginas=listagem.pages,
            total=listagem.total,
        )
