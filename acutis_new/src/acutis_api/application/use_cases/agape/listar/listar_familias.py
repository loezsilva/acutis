import math

from acutis_api.application.utils.funcoes_auxiliares import calcular_idade
from acutis_api.communication.requests.agape import (
    ListarFamiliasAgapeQueryPaginada,
)
from acutis_api.communication.responses.agape import (
    FamiliaAgapeResponse,
    ListarFamiliasAgapeResponsePaginada,
    MembroFamiliaAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class ListarFamiliasUseCase:
    """
    Caso de uso para listar as famílias cadastradas:
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self, filtros: ListarFamiliasAgapeQueryPaginada
    ) -> ListarFamiliasAgapeResponsePaginada:
        # Executa consulta ao repositório para obter instâncias do ciclo
        instancias, total = self.__repository.listar_familias(filtros)

        # Cria resposta paginada
        pagina_atual = filtros.pagina
        paginas_total = (
            math.ceil(total / filtros.por_pagina) if filtros.por_pagina else 1
        )

        return ListarFamiliasAgapeResponsePaginada(
            pagina=pagina_atual,
            paginas=paginas_total,
            total=total,
            resultados=[
                FamiliaAgapeResponse(
                    id=instancia.id,
                    nome_familia=instancia.nome_familia,
                    cadastrada_por=instancia.cadastrada_por,
                    criado_em=instancia.criado_em,
                    endereco_id=instancia.fk_endereco_id,
                    observacao=instancia.observacao,
                    deletado_em=instancia.deletado_em,
                    membros=[
                        MembroFamiliaAgapeResponse(
                            id=membro_instancia.id,
                            cpf=membro_instancia.cpf,
                            nome=membro_instancia.nome,
                            email=membro_instancia.email,
                            telefone=membro_instancia.telefone,
                            ocupacao=membro_instancia.ocupacao,
                            renda=membro_instancia.renda,
                            responsavel=membro_instancia.responsavel,
                            idade=calcular_idade(
                                membro_instancia.data_nascimento
                            ),
                        ).model_dump()
                        for membro_instancia in (
                            self.__repository.listar_membros_por_familia_id(
                                familia_id=instancia.id
                            )
                        )
                    ],
                ).model_dump()
                for instancia in instancias
            ],
        )
