from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin.doacoes.listar import (
    ListarDoacoesUseCase,
)
from acutis_api.communication.requests.admin_doacoes import ListarDoacoesQuery
from acutis_api.communication.responses.admin_doacoes import (
    ListarDoacoesResponse,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.admin_doacoes import (
    AdminDoacoesRepository,
)

admin_doacoes_bp = Blueprint(
    'admin_doacoes_bp', __name__, url_prefix='/admin/doacoes'
)


@admin_doacoes_bp.get('/listar-doacoes')
@swagger.validate(
    query=ListarDoacoesQuery,
    resp=Response(
        HTTP_200=ListarDoacoesResponse,
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def listar_doacoes():
    """Lista todas as doações"""
    try:
        filtros = ListarDoacoesQuery.model_validate(
            flask_request.args.to_dict()
        )

        repository = AdminDoacoesRepository(database)
        usecase = ListarDoacoesUseCase(repository)

        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
