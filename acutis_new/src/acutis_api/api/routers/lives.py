from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.lives.deletar import (
    DeletarProgramacaoLiveUseCase,
)
from acutis_api.application.use_cases.lives.editar import (
    EditarProgramacaoLiveUseCase,
)
from acutis_api.application.use_cases.lives.listar import (
    ObterAudienciaLivesUseCase,
    ObterCanalUseCase,
    ObterDatasLivesOcorridasUseCase,
    ObterHistogramaLiveUseCase,
    ObterLivesProgramadasUseCase,
    ObterTodasLivesAvulsasUseCase,
    ObterTodasLivesRecorrentesUseCase,
)
from acutis_api.application.use_cases.lives.registrar import (
    CriarCanalUseCase,
    RegistrarLiveUseCase,
)
from acutis_api.communication.requests.lives import (
    DeletarProgramacaoLiveRequest,
    EditarProgramacaoLiveRequest,
    ObterAudienciaLivesRequest,
    ObterCanalRequest,
    ObterHistogramaLiveRequest,
    ObterLivesProgramadasRequest,
    ObterTodasLivesAvulsasRequest,
    ObterTodasLivesRecorrentesRequest,
    RegistrarCanalRequest,
    RegistrarLiveRequest,
)
from acutis_api.communication.responses.lives import (
    ListaObterCanalResponse,
    ListaObterLivesProgramadasResponse,
    ObterAudienciaLivesResponse,
    ObterDatasLivesOcorridasResponse,
    ObterHistogramaLiveResponse,
    ObterTodasLivesAvulsasResponse,
    ObterTodasLivesRecorrentesResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.lives import LivesRepository

lives_bp = Blueprint('lives_bp', __name__, url_prefix='/admin/lives')


@lives_bp.post('/criar-canal')
@swagger.validate(
    json=RegistrarCanalRequest,
    resp=Response(
        HTTP_201=ResponsePadraoSchema,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def criar_canal():
    """
    Rota de registrar o canal de uma rede social para fazer live
    """
    try:
        request = RegistrarCanalRequest.model_validate(
            flask_request.get_json()
        )

        repository = LivesRepository(database)
        usecase = CriarCanalUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@lives_bp.get('/obter-canal')
@swagger.validate(
    query=ObterCanalRequest,
    resp=Response(
        HTTP_200=ListaObterCanalResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_canal():
    """
    Rota de obter os canais para live que estão registrados
    """
    try:
        request = ObterCanalRequest.model_validate(
            flask_request.args.to_dict()
        )

        repository = LivesRepository(database)
        usecase = ObterCanalUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@lives_bp.post('/registrar-live')
@swagger.validate(
    json=RegistrarLiveRequest,
    resp=Response(
        HTTP_201=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def registrar_live():
    """
    Rota de registrar lives, sendo elas avulsas ou recorrentes
    """
    try:
        request = RegistrarLiveRequest.model_validate(flask_request.get_json())

        repository = LivesRepository(database)
        usecase = RegistrarLiveUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@lives_bp.get('/obter-lives-programadas')
@swagger.validate(
    query=ObterLivesProgramadasRequest,
    resp=Response(
        HTTP_200=ListaObterLivesProgramadasResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_lives_programadas():
    """
    Rota de obter as lives programadas, sendo elas avulsas ou recorrentes
    """
    try:
        request = ObterLivesProgramadasRequest.model_validate(
            flask_request.args.to_dict()
        )

        repository = LivesRepository(database)
        usecase = ObterLivesProgramadasUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@lives_bp.put('/editar-programacao-live/<uuid:programacao_id>')
@swagger.validate(
    json=EditarProgramacaoLiveRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_404=ErroPadraoResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def editar_programacao_live(programacao_id):
    """
    Rota de edição da programação de uma live (avulsa ou periódica)
    """
    try:
        request = EditarProgramacaoLiveRequest.model_validate(
            flask_request.get_json()
        )

        repository = LivesRepository(database)
        usecase = EditarProgramacaoLiveUseCase(repository)

        response = usecase.execute(request, programacao_id)

        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@lives_bp.delete('/deletar-programacao-live')
@swagger.validate(
    json=DeletarProgramacaoLiveRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def deletar_programacao_live():
    """
    Rota de deletar lives programadas
    """
    try:
        request = DeletarProgramacaoLiveRequest.model_validate(
            flask_request.get_json()
        )

        repository = LivesRepository(database)
        usecase = DeletarProgramacaoLiveUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@lives_bp.get('/obter-todas-lives-recorrentes')
@swagger.validate(
    query=ObterTodasLivesRecorrentesRequest,
    resp=Response(
        HTTP_201=ObterTodasLivesRecorrentesResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_todas_lives_recorrentes():
    """
    Rota de listar todas as lives recorrentes programadas
    """
    try:
        request = ObterTodasLivesRecorrentesRequest.model_validate(
            flask_request.args.to_dict()
        )

        repository = LivesRepository(database)
        usecase = ObterTodasLivesRecorrentesUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@lives_bp.get('/obter-todas-lives-avulsas')
@swagger.validate(
    query=ObterTodasLivesAvulsasRequest,
    resp=Response(
        HTTP_200=ObterTodasLivesAvulsasResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_todas_lives_avulsas():
    """
    Rota para listar todas as lives avulsas programadas
    """
    try:
        request = ObterTodasLivesAvulsasRequest.model_validate(
            flask_request.args.to_dict()
        )

        repository = LivesRepository(database)
        usecase = ObterTodasLivesAvulsasUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@lives_bp.get('/obter-audiencia-lives')
@swagger.validate(
    query=ObterAudienciaLivesRequest,
    resp=Response(
        HTTP_200=ObterAudienciaLivesResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_audiencia_lives():
    """
    Rota para listar a contagem de audiência de lives passadas
    """
    try:
        request = ObterAudienciaLivesRequest.model_validate(
            flask_request.args.to_dict()
        )

        repository = LivesRepository(database)
        usecase = ObterAudienciaLivesUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@lives_bp.get('/obter-datas-lives-ocorridas')
@swagger.validate(
    resp=Response(
        HTTP_200=ObterDatasLivesOcorridasResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_datas_lives_ocorridas():
    """
    Rota para obter as datas distintas de registros de audiência de lives
    """
    try:
        repository = LivesRepository(database)
        usecase = ObterDatasLivesOcorridasUseCase(repository)

        response = usecase.execute()

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@lives_bp.get('/obter-dados-histograma')
@swagger.validate(
    query=ObterHistogramaLiveRequest,
    resp=Response(
        HTTP_200=ObterHistogramaLiveResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Lives'],
)
@jwt_required()
def obter_histograma_live():
    """
    Rota para retornar os dados de histograma de uma live através
    da pesquisa com seu título e rede social.
    """
    try:
        request = ObterHistogramaLiveRequest.model_validate({
            'filtro_titulo_live': flask_request.args.get('filtro_titulo_live'),
            'filtro_rede_social': flask_request.args.get('filtro_rede_social'),
        })

        repository = LivesRepository(database)

        usecase = ObterHistogramaLiveUseCase(repository)

        response = usecase.execute(request)

        return response, HTTPStatus.OK

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
