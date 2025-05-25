from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.campanha.atualizar.campanha import (
    AtualizarCampanhaUseCase,
)
from acutis_api.application.use_cases.campanha.listar import (
    BuscaCampanhaPorNomeUseCase,
    ListaDeCampanhasUseCase,
)
from acutis_api.application.use_cases.campanha.listar.campanha_por_id import (
    BuscaCampanhaPorIdUseCase,
)
from acutis_api.application.use_cases.campanha.listar.campanhas import (
    ListarCampanhasUseCase,
)
from acutis_api.application.use_cases.campanha.registrar.cadastro_por_campanha import (  # noqa
    CadastroPorCampanhaUseCase,
)
from acutis_api.application.use_cases.campanha.registrar.campanha import (
    RegistrarCampanhaUseCase,
)
from acutis_api.communication.requests.campanha import (
    CadastroPorCampanhaFormData,
    ListarCampanhasQuery,
    RegistrarNovaCampanhaFormData,
)
from acutis_api.communication.responses.campanha import (
    ListaCampanhaPorIdResponse,
    ListaCampanhaPorNomeResponse,
    ListaDeCampanhasResponse,
    ListagemCompletaDeCampanhaResponse,
    RegistrarNovaCampanhaResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.campanha import CampanhaRepository
from acutis_api.infrastructure.repositories.membros import MembrosRepository
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.services.itau import ItauPixService

admin_campanha_bp = Blueprint(
    'admin_campanha_bp', __name__, url_prefix='/admin/campanhas'
)


@admin_campanha_bp.post('/registrar-campanha')
@swagger.validate(
    form=RegistrarNovaCampanhaFormData,
    resp=Response(HTTP_201=RegistrarNovaCampanhaResponse),
    tags=['Campanhas'],
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
            dados_da_landing_page=flask_request.form.get(
                'dados_da_landing_page'
            ),
            foto_capa=flask_request.files.get('foto_capa'),
        )

        s3_service = file_service_factory()
        payment_service = ItauPixService()
        repository = CampanhaRepository(database)
        usecase = RegistrarCampanhaUseCase(
            repository, s3_service, payment_service
        )
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/listar-campanhas')
@swagger.validate(
    query=ListarCampanhasQuery,
    resp=Response(HTTP_200=ListagemCompletaDeCampanhaResponse),
    tags=['Campanhas'],
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
    tags=['Campanhas'],
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
            dados_da_landing_page=flask_request.form.get(
                'dados_da_landing_page'
            ),
        )

        s3_service = file_service_factory()
        payment_service = ItauPixService()
        repository = CampanhaRepository(database)
        usecase = AtualizarCampanhaUseCase(
            repository, s3_service, payment_service
        )
        response = usecase.execute(request, fk_campanha_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/buscar-campanha-por-id/<uuid:fk_campanha_id>')
@swagger.validate(
    resp=Response(HTTP_201=ListaCampanhaPorIdResponse),
    tags=['Campanhas'],
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


@admin_campanha_bp.get('/buscar-campanha-por-nome/<string:nome_campanha>')
@swagger.validate(
    resp=Response(HTTP_200=ListaCampanhaPorNomeResponse),
    tags=['Campanhas'],
)
def busca_campanha_por_nome(nome_campanha):
    """
    Busca campanha por nome
    """
    try:
        repository = CampanhaRepository(database)
        usecase = BuscaCampanhaPorNomeUseCase(repository)
        return usecase.execute(nome_campanha), HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_campanha_bp.post('/cadastro-por-campanha/<uuid:campanha_id>')
@swagger.validate(
    form=CadastroPorCampanhaFormData,
    resp=Response(HTTP_201=ResponsePadraoSchema, HTTP_500=ErroPadraoResponse),
    tags=['Campanhas'],
)
@jwt_required(optional=True)
def cadastro_por_campanha(campanha_id):
    """
    Realiza o cadastro de um membro por meio de uma campanha
    """
    try:
        request = CadastroPorCampanhaFormData(
            nome=flask_request.form.get('nome'),
            nome_social=flask_request.form.get('nome_social'),
            email=flask_request.form.get('email'),
            numero_documento=flask_request.form.get('numero_documento'),
            pais=flask_request.form.get('pais'),
            telefone=flask_request.form.get('telefone'),
            data_nascimento=flask_request.form.get('data_nascimento'),
            sexo=flask_request.form.get('sexo'),
            origem_cadastro=flask_request.form.get('origem_cadastro'),
            senha=flask_request.form.get('senha'),
            foto=flask_request.files.get('foto'),
            endereco=flask_request.form.get('endereco'),
            superior=flask_request.form.get('superior'),
            campos_adicionais=flask_request.form.get('campos_adicionais'),
        )
        s3_service = file_service_factory()
        membro_repository = MembrosRepository(database)
        usecase = CadastroPorCampanhaUseCase(membro_repository, s3_service)
        response = usecase.execute(request, campanha_id)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@admin_campanha_bp.get('/lista-de-campanhas')
@swagger.validate(
    resp=Response(HTTP_200=ListaDeCampanhasResponse),
    tags=['Campanhas'],
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
