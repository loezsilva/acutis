import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin.benfeitores.buscar import (
    BuscarCardsBenfeitoresUseCase,
    BuscarInformacoesBenfeitorUseCase,
)
from acutis_api.application.use_cases.admin.benfeitores.listar import (
    ListarBenfeitoresUseCase,
    ListarDoacoesAnonimasBenfeitorUseCase,
)
from acutis_api.communication.requests.admin_benfeitores import (
    ListarBenfeitoresQuery,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.communication.responses.admin_benfeitores import (
    BuscarCardsBenfeitoresResponse,
    BuscarInformacoesBenfeitorResponse,
    ListarBenfeitoresResponse,
    ListarDoacoesAnonimasBenfeitorResponse,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.admin_benfeitores import (
    AdminBenfeitoresRepository,
)

admin_benfeitores_bp = Blueprint(
    'admin_benfeitores_bp', __name__, url_prefix='/admin/benfeitores'
)


@admin_benfeitores_bp.get('/buscar-cards-benfeitores')
@swagger.validate(
    resp=Response(HTTP_200=BuscarCardsBenfeitoresResponse),
    tags=['Admin - Benfeitores'],
)
@jwt_required()
def buscar_cards_doacoes_benfeitores():
    """Retorna os cards de doações dos benfeitores"""
    try:
        repository = AdminBenfeitoresRepository(database)
        usecase = BuscarCardsBenfeitoresUseCase(repository)

        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_benfeitores_bp.get('/listar-benfeitores')
@swagger.validate(
    query=ListarBenfeitoresQuery,
    resp=Response(
        HTTP_200=ListarBenfeitoresResponse,
    ),
    tags=['Admin - Benfeitores'],
)
@jwt_required()
def listar_benfeitores():
    """Lista todos os benfeitores que possuem doações anonimas"""
    try:
        filtros = ListarBenfeitoresQuery.model_validate(
            flask_request.args.to_dict()
        )

        repository = AdminBenfeitoresRepository(database)
        usecase = ListarBenfeitoresUseCase(repository)

        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_benfeitores_bp.get('/buscar-informacoes-benfeitor/<uuid:benfeitor_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarInformacoesBenfeitorResponse,
    ),
    tags=['Admin - Benfeitores'],
)
@jwt_required()
def buscar_informacao_benfeitor(benfeitor_id: uuid.UUID):
    """Busca as informações do benfeitor pelo ID"""
    try:
        repository = AdminBenfeitoresRepository(database)
        usecase = BuscarInformacoesBenfeitorUseCase(repository)

        response = usecase.execute(benfeitor_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_benfeitores_bp.get(
    '/listar-doacoes-anonimas-benfeitor/<uuid:benfeitor_id>'
)
@swagger.validate(
    query=PaginacaoQuery,
    resp=Response(HTTP_200=ListarDoacoesAnonimasBenfeitorResponse),
    tags=['Admin - Benfeitores'],
)
@jwt_required()
def listar_doacoes_anonimas_benfeitor(benfeitor_id: uuid.UUID):
    """Lista as doações anonimas do benfeitor pelo ID"""
    try:
        filtros = PaginacaoQuery.model_validate(flask_request.args.to_dict())

        repository = AdminBenfeitoresRepository(database)
        usecase = ListarDoacoesAnonimasBenfeitorUseCase(repository)

        response = usecase.execute(filtros, benfeitor_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
