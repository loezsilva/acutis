import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin import (
    BuscarLeadsMesUseCase,
    BuscarMembrosMesUseCase,
    BuscarTotalLeadsUseCase,
    BuscarTotalMembrosUseCase,
    BuscarUsuarioPorIDUseCase,
    ListarLeadsMembrosUseCase,
)
from acutis_api.application.use_cases.admin.membros_oficiais.deletar import (
    AdminExcluirContaUseCase,
)
from acutis_api.communication.requests.admin_membros import (
    ListarLeadsMembrosQuery,
)
from acutis_api.communication.responses.admin_membros import (
    BuscarDetalhesDoLeadResponse,
    BuscarLeadsMesResponse,
    BuscarMembrosMesResponse,
    BuscarTotalLeadsResponse,
    BuscarTotalMembrosResponse,
    ListarLeadsMembrosResponse,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
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


@admin_membros_bp.delete('/excluir-conta/<uuid:fk_lead_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
    ),
    tags=['Admin - Membros'],
)
@jwt_required()
def admin_excluir_conta(fk_lead_id: uuid.UUID):
    """
    Exclui a conta do lead pelo UUID
    """
    try:
        repository = AdminMembrosRepository(database)
        usecase = AdminExcluirContaUseCase(repository)
        usecase.execute(fk_lead_id)
        return {'msg': 'Conta deletada com sucesso'}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@admin_membros_bp.get('/buscar-total-leads')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarTotalLeadsResponse,
    ),
    tags=['Admin - Membros'],
)
def buscar_total_leads():
    """
    Busca o total de leads
    """
    try:
        repository = AdminMembrosRepository(database)
        usecase = BuscarTotalLeadsUseCase(repository)

        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_membros_bp.get('/buscar-total-membros')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarTotalMembrosResponse,
    ),
    tags=['Admin - Membros'],
)
def buscar_total_membros():
    """
    Busca o total de membros
    """
    try:
        repository = AdminMembrosRepository(database)
        usecase = BuscarTotalMembrosUseCase(repository)

        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_membros_bp.get('/buscar-leads-mes')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarLeadsMesResponse,
    ),
    tags=['Admin - Membros'],
)
def buscar_leads_mes():
    """
    Busca o total de leads do mês
    """
    try:
        repository = AdminMembrosRepository(database)
        usecase = BuscarLeadsMesUseCase(repository)

        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_membros_bp.get('/buscar-membros-mes')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarMembrosMesResponse,
    ),
    tags=['Admin - Membros'],
)
def buscar_membros_mes():
    """
    Busca o total de membros do mês
    """
    try:
        repository = AdminMembrosRepository(database)
        usecase = BuscarMembrosMesUseCase(repository)

        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
