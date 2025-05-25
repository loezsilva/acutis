from flask import request
from flask_jwt_extended import current_user
from exceptions.error_types.http_forbidden import ForbiddenError
from handlers.vocacional.utils.verificar_permissoes_vocacional import (
    verificar_permissoes_vocacional,
)
from models.schemas.vocacional.get.listar_pre_cadastros_schema import (
    ListarPreCadastrosQuery,
)
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class ListarPreCadastros:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self):

        filtros_permissoes = verificar_permissoes_vocacional()

        filtros = ListarPreCadastrosQuery.parse_obj(request.args)
        return self.__vocacional_repository.get_pre_cadastro_vocacional(
            filtros, filtros.page, filtros.per_page, filtros_permissoes
        )
