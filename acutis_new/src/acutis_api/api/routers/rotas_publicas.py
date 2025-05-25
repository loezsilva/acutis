from http import HTTPStatus

from flask import Blueprint
from spectree import Response

from acutis_api.application.use_cases.publico import (
    BuscaCargoSuperiorUseCase,
)
from acutis_api.communication.responses.publico import (
    BuscaCargoSuperiorResponse,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.membros_oficiais import (
    MembrosOficiaisRepository,
)

rotas_publicas_bp = Blueprint(
    'rotas_publicas_bp', __name__, url_prefix='/rotas-publicas'
)


@rotas_publicas_bp.get('/busca-cargo-superior/<uuid:fk_cargo_oficial_id>')
@swagger.validate(
    resp=Response(HTTP_200=BuscaCargoSuperiorResponse),
    tags=['Rotas Publicas'],
)
def busca_cargo_superior(fk_cargo_oficial_id: str):
    """
    Retorna o cargo superior e uma lista de superiores
    """
    try:
        repository = MembrosOficiaisRepository(database)
        usecase = BuscaCargoSuperiorUseCase(repository)
        response = usecase.execute(fk_cargo_oficial_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)
