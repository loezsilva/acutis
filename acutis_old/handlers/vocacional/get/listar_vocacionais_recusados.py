from flask import request
from handlers.vocacional.utils.verificar_permissoes_vocacional import verificar_permissoes_vocacional
from models.schemas.vocacional.get.listar_vocacionais_recusados_schema import (
    VocacionaisRecusadosQuery,
)
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class ListarVocacionaisRecusados:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self):
        
        filtros_permissoes = verificar_permissoes_vocacional()

        
        filtros = VocacionaisRecusadosQuery.parse_obj(request.args)
        return self.__vocacional_repository.get_vocacionais_recusados(
            filtros, filtros.page, filtros.per_page, filtros_permissoes
        )
