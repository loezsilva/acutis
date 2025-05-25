import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin import (
    BuscarUsuarioPorIDUseCase,
    ListarLeadsMembrosUseCase,
)
from acutis_api.communication.requests.admin_membros import (
    ListarLeadsMembrosQuery,
)
from acutis_api.communication.responses.admin_membros import (
    BuscarDetalhesDoLeadResponse,
    ListarLeadsMembrosResponse,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.admin_membros import (
    AdminMembrosRepository,
)
from acutis_api.infrastructure.services.factories import file_service_factory

admin_membros_bp = Blueprint(
    'admin_membros_bp', __name__, url_prefix='/admin/membros'
)


@admin_membros_bp.get('/listar-leads-e-membros')
@swagger.validate(
    query=ListarLeadsMembrosQuery,
    resp=Response(HTTP_200=ListarLeadsMembrosResponse),
    tags=['Admin - Membros'],
)
@jwt_required()
def listar_leads_e_membros():
    """
    Lista todos os leads e membros em Admin
    """
    try:
        filtros = ListarLeadsMembrosQuery.model_validate(
            flask_request.args.to_dict()
        )

        repository = AdminMembrosRepository(database)
        file_service = file_service_factory()
        usecase = ListarLeadsMembrosUseCase(repository, file_service)

        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_membros_bp.get('/buscar-lead/<uuid:uuid>')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarDetalhesDoLeadResponse,
    ),
    tags=['Admin - Membros'],
)
def buscar_lead_por_id(uuid: uuid.UUID):
    """
    Busca os dados do lead pelo UUID
    """
    try:
        repository = AdminMembrosRepository(database)
        file_service = file_service_factory()
        usecase = BuscarUsuarioPorIDUseCase(repository, file_service)

        response = usecase.execute(uuid)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
