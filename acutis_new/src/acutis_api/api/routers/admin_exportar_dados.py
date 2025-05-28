from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin.exportar_dados import (
    ExportarLeadsUseCase,
    ExportarMembrosOficiaisUseCase,
)
from acutis_api.application.use_cases.admin.exportar_dados.benfeitores import (
    ExportarBenfeitoresUseCase,
)
from acutis_api.application.use_cases.admin.exportar_dados.doacoes import (
    ExportarDoacoesUseCase,
)
from acutis_api.application.use_cases.admin.exportar_dados.membros import (
    ExportarMembrosUseCase,
)
from acutis_api.communication.requests.admin_exportar_dados import (
    ExportaLeadsRequest,
    ExportarBenfeitoresQuery,
    ExportarDadosMembroOficialRequest,
    ExportarDoacoesQuery,
    ExportarMembrosRequest,
)
from acutis_api.communication.responses.admin_exportar_dados import (
    ExportarDadosResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.admin_exportar_dados import (
    ExportarDadosRepository,
)

admin_exportar_dados_bp = Blueprint(
    'admin_exportar_dados_bp', __name__, url_prefix='/admin/exportar'
)


@admin_exportar_dados_bp.get('/leads')
@swagger.validate(
    query=ExportaLeadsRequest,
    resp=Response(HTTP_200=None, HTTP_500=ResponsePadraoSchema),
    tags=['Admin - Exportar Dados'],
)
@jwt_required()
def exportar_leads():
    """Exporta os leads"""
    try:
        request = ExportaLeadsRequest.model_validate(
            flask_request.args.to_dict()
        )
        repository = ExportarDadosRepository(database)
        usecase = ExportarLeadsUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_exportar_dados_bp.get('/membros')
@swagger.validate(
    query=ExportarMembrosRequest,
    resp=Response(
        HTTP_200=ExportarDadosResponse,
        HTTP_500=ResponsePadraoSchema,
    ),
    tags=['Admin - Exportar Dados'],
)
@jwt_required()
def exportar_membros():
    """Exporta os membros"""
    try:
        request = ExportarMembrosRequest.model_validate(
            flask_request.args.to_dict()
        )
        repository = ExportarDadosRepository(database)
        usecase = ExportarMembrosUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_exportar_dados_bp.get('/membros-oficiais')
@swagger.validate(
    query=ExportarDadosMembroOficialRequest,
    resp=Response(HTTP_200=ExportarDadosResponse, HTTP_500=ErroPadraoResponse),
    tags=['Admin - Exportar Dados'],
)
@jwt_required()
def exportar_membros_oficiais():
    """Exporta os membros oficiais"""
    try:
        request = ExportarDadosMembroOficialRequest.model_validate(
            flask_request.args.to_dict()
        )
        repository = ExportarDadosRepository(database)
        usecase = ExportarMembrosOficiaisUseCase(repository)
        return usecase.execute(request), HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_exportar_dados_bp.get('/doacoes')
@swagger.validate(
    query=ExportarDoacoesQuery,
    resp=Response(HTTP_200=ExportarDadosResponse, HTTP_500=ErroPadraoResponse),
    tags=['Admin - Exportar Dados'],
)
@jwt_required()
def exportar_doacoes():
    """Exporta as doações"""
    try:
        request = flask_request.args.to_dict(flat=True)
        request['colunas'] = flask_request.args.getlist('colunas')
        request = ExportarDoacoesQuery.model_validate(request)

        repository = ExportarDadosRepository(database)
        usecase = ExportarDoacoesUseCase(repository)
        return usecase.execute(request), HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_exportar_dados_bp.get('/benfeitores')
@swagger.validate(
    query=ExportarBenfeitoresQuery,
    resp=Response(HTTP_200=ExportarDadosResponse, HTTP_500=ErroPadraoResponse),
    tags=['Admin - Exportar Dados'],
)
@jwt_required()
def exportar_benfeitores():
    """Exporta os benfeitores"""
    try:
        request = flask_request.args.to_dict(flat=True)
        request['colunas'] = flask_request.args.getlist('colunas')
        request = ExportarBenfeitoresQuery.model_validate(request)

        repository = ExportarDadosRepository(database)
        usecase = ExportarBenfeitoresUseCase(repository)
        return usecase.execute(request), HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
