from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.campanha.listar import (
    BuscaCampanhaPorNomeUseCase,
)
from acutis_api.application.use_cases.campanha.registrar import (
    CadastroPorCampanhaUseCase,
)
from acutis_api.application.use_cases.publico import (
    BuscaCargoSuperiorUseCase,
)
from acutis_api.application.use_cases.rotas_publicas import (
    LandingpageDaCampanhaUseCase,
)
from acutis_api.communication.requests.campanha import (
    CadastroPorCampanhaFormData,
)
from acutis_api.communication.responses.campanha import (
    ListaCampanhaPorNomeResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.communication.responses.publico import (
    BuscaCargoSuperiorResponse,
)
from acutis_api.communication.responses.rotas_publicas import (
    BuscaLandingPageDaCampanhaResponse,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.campanha import CampanhaRepository
from acutis_api.infrastructure.repositories.membros import MembrosRepository
from acutis_api.infrastructure.repositories.membros_oficiais import (
    MembrosOficiaisRepository,
)
from acutis_api.infrastructure.services.factories import file_service_factory

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


@rotas_publicas_bp.get('/buscar-campanha-por-nome/<string:nome_campanha>')
@swagger.validate(
    resp=Response(HTTP_200=ListaCampanhaPorNomeResponse),
    tags=['Rotas Publicas'],
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


@rotas_publicas_bp.post('/cadastro-por-campanha/<uuid:campanha_id>')
@swagger.validate(
    form=CadastroPorCampanhaFormData,
    resp=Response(HTTP_201=ResponsePadraoSchema, HTTP_500=ErroPadraoResponse),
    tags=['Rotas Publicas'],
)
@jwt_required(optional=True)
def cadastro_por_campanha(campanha_id):
    """
    Realiza o cadastro de um membro por meio de uma campanha
    """
    try:
        request = CadastroPorCampanhaFormData.model_validate(
            flask_request.form.to_dict()
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


@rotas_publicas_bp.get('/busca-landingpage-por-nome/<nome_campanha>')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscaLandingPageDaCampanhaResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Rotas Publicas'],
)
def get_landingpage_por_nome(nome_campanha):
    """
    Busca landing page pelo nome da campanha
    """
    try:
        repository = CampanhaRepository(database)
        usecase = LandingpageDaCampanhaUseCase(repository)
        response = usecase.execute(nome_campanha)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response
