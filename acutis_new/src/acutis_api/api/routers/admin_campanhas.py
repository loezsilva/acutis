import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.campanha.atualizar import (
    AtualizarLandPageCampanhaUseCase,
)
from acutis_api.application.use_cases.campanha.atualizar.campanha import (
    AtualizarCampanhaUseCase,
)
from acutis_api.application.use_cases.campanha.listar import (
    CadastrosCampanhaPorPeriodoUseCase,
    ListaDeCampanhasUseCase,
    ListarDoacoesCampanhaUseCase,
    PainelCampanhasUseCase,
)
from acutis_api.application.use_cases.campanha.listar.campanha_por_id import (
    BuscaCampanhaPorIdUseCase,
)
from acutis_api.application.use_cases.campanha.listar.campanhas import (
    ListarCampanhasUseCase,
)
from acutis_api.application.use_cases.campanha.registrar import (  # noqa
    CadastroPorCampanhaUseCase,
    SalvarLandPageCampanhaUseCase,
)
from acutis_api.application.use_cases.campanha.registrar.campanha import (
    RegistrarCampanhaUseCase,
)
from acutis_api.communication.requests.campanha import (
    AtualizarLandpageRequest,
    ListarCampanhasQuery,
    PainelCampanhasRequest,
    RegistrarNovaCampanhaFormData,
    SalvarLandpageRequest,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.communication.responses.campanha import (
    CadastrosCampanhaPorPeriodoResponse,
    ListaCampanhaPorIdResponse,
    ListaDeCampanhasResponse,
    ListagemCompletaDeCampanhaResponse,
    ListarDoacoesCampanhaResponse,
    PainelCampanhasResponse,
    RegistrarNovaCampanhaResponse,
)
from acutis_api.communication.responses.padrao import (
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.campanha import CampanhaRepository
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.services.itau import ItauPixService

admin_campanha_bp = Blueprint(
    'admin_campanha_bp', __name__, url_prefix='/admin/campanhas'
)


@admin_campanha_bp.post('/registrar-campanha')
@swagger.validate(
    form=RegistrarNovaCampanhaFormData,
    resp=Response(HTTP_201=RegistrarNovaCampanhaResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def registrar_campanha():
    """
    Cria uma nova campanha
    """
    try:
        request = RegistrarNovaCampanhaFormData(
            dados_da_campanha=flask_request.form['dados_da_campanha'],
            campos_adicionais=flask_request.form.get('campos_adicionais'),
            foto_capa=flask_request.files.get('foto_capa'),
        )

        s3_service = file_service_factory()
        itau_api = ItauPixService()
        repository = CampanhaRepository(database)
        usecase = RegistrarCampanhaUseCase(repository, s3_service, itau_api)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/listar-campanhas')
@swagger.validate(
    query=ListarCampanhasQuery,
    resp=Response(HTTP_200=ListagemCompletaDeCampanhaResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def listar_campanhas():
    """
    Lista campanhas no admin
    """
    try:
        request = ListarCampanhasQuery(**flask_request.args)
        s3_service = file_service_factory()
        repository = CampanhaRepository(database)
        usecase = ListarCampanhasUseCase(s3_service, repository)
        response = usecase.execute(request)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.put('/atualizar-campanha/<uuid:fk_campanha_id>')
@swagger.validate(
    form=RegistrarNovaCampanhaFormData,
    resp=Response(HTTP_201=RegistrarNovaCampanhaResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def atualizar_campanha(fk_campanha_id):
    """
    Atualiza campanha
    """
    try:
        request = RegistrarNovaCampanhaFormData(
            dados_da_campanha=flask_request.form.get('dados_da_campanha'),
            campos_adicionais=flask_request.form.get('campos_adicionais'),
            foto_capa=flask_request.files.get('foto_capa'),
        )

        s3_service = file_service_factory()
        itau_api = ItauPixService()
        repository = CampanhaRepository(database)
        usecase = AtualizarCampanhaUseCase(repository, s3_service, itau_api)
        response = usecase.execute(request, fk_campanha_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/buscar-campanha-por-id/<uuid:fk_campanha_id>')
@swagger.validate(
    resp=Response(HTTP_200=ListaCampanhaPorIdResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def busca_campanha_por_id(fk_campanha_id):
    """
    Busca campanha por id
    """
    try:
        s3_service = file_service_factory()
        repository = CampanhaRepository(database)
        usecase = BuscaCampanhaPorIdUseCase(repository, s3_service)
        return usecase.execute(fk_campanha_id), HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_campanha_bp.get('/lista-de-campanhas')
@swagger.validate(
    resp=Response(HTTP_200=ListaDeCampanhasResponse),
    tags=['Admin - Campanhas'],
)
def lista_de_campanhas():
    """
    Busca campanha por nome
    """
    try:
        repository = CampanhaRepository(database)
        usecase = ListaDeCampanhasUseCase(repository)
        return usecase.execute(), HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_campanha_bp.post('/painel-campanhas')
@swagger.validate(
    form=PainelCampanhasRequest,
    resp=Response(HTTP_200=PainelCampanhasResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def painel_campanhas():
    """
    Busca campanhas para o painel
    """
    try:
        request = PainelCampanhasRequest.model_validate(flask_request.json)
        repository = CampanhaRepository(database)
        usecase = PainelCampanhasUseCase(repository)
        return usecase.execute(request), HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_campanha_bp.post('/registrar-landingpage')
@swagger.validate(
    json=SalvarLandpageRequest,
    resp=Response(HTTP_200=ResponsePadraoSchema),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def salvar_landpage():
    """
    Salva a landpage da campanha
    """
    try:
        request = SalvarLandpageRequest.model_validate(
            flask_request.get_json()
        )
        repository = CampanhaRepository(database)
        usecase = SalvarLandPageCampanhaUseCase(repository)
        usecase.execute(request)
        return {'msg': 'Landpage salva com sucesso.'}, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.put('/atualizar-landingpage')
@swagger.validate(
    json=AtualizarLandpageRequest,
    resp=Response(HTTP_200=ResponsePadraoSchema),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def atualizar_landpage():
    try:
        repository = CampanhaRepository(database)
        request = AtualizarLandpageRequest.model_validate(
            flask_request.get_json()
        )
        usecase = AtualizarLandPageCampanhaUseCase(repository)
        usecase.execute(request)
        return {'msg': 'Landpage atualizada com sucesso.'}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/listar-doacoes-campanha/<uuid:campanha_id>')
@swagger.validate(
    query=PaginacaoQuery,
    resp=Response(HTTP_200=ListarDoacoesCampanhaResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def listar_doacoes_campanha(campanha_id: uuid.UUID):
    """Lista todas as doações pagas feitas para a campanha pelo ID"""
    try:
        filtros = PaginacaoQuery.model_validate(flask_request.args.to_dict())

        repository = CampanhaRepository(database)
        usecase = ListarDoacoesCampanhaUseCase(repository)

        response = usecase.execute(filtros, campanha_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/cadastros-campanha-por-periodo/<uuid:campanha_id>')
@swagger.validate(
    resp=Response(HTTP_200=CadastrosCampanhaPorPeriodoResponse),
    tags=['Admin - Campanhas'],
)
@jwt_required()
def cadastros_campanha_por_periodo(campanha_id: uuid.UUID):
    """
    Lista a quantidade de cadastros de uma campanha nas últimas 24h,
    últimos 7 dias, e último mês.
    """
    try:
        repository = CampanhaRepository(database)
        usecase = CadastrosCampanhaPorPeriodoUseCase(repository)

        response = usecase.execute(campanha_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
