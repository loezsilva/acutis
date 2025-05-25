from flask import request
from handlers.vocacional.utils.verificar_permissoes_vocacional import (
    verificar_permissoes_vocacional,
)
from models.schemas.vocacional.get.listar_fichas_vocacionais_schema import (
    ListarFichasVocacionaisQuery,
)
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class ListarFichasVocacionais:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self):

        filtros_permissoes = verificar_permissoes_vocacional()


        filtros = ListarFichasVocacionaisQuery.parse_obj(request.args)
        return self.__vocacional_repository.get__all_fichas_vocacionais(
            filtros, filtros.page, filtros.per_page, filtros_permissoes
        )
