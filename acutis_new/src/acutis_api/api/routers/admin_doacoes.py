from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin.doacoes.atualizar import (
    ContabilizarDoacoesUseCase,
)
from acutis_api.application.use_cases.admin.doacoes.listar import (
    CardDoacoesDoDiaUseCase,
    CardDoacoesDoMesUseCase,
    ListarDoacoesUseCase,
    MediaDiariaUseCase,
    MediaMensalUseCase,
    RecorrenciaNaoEfetuadaUseCase,
    RecorrenciasCanceladasUseCase,
    RecorrenciasEfetuadasUseCase,
    RecorrenciasLembretesEfetivosUseCase,
    RecorrenciasPrevistasUseCase,
    RecorrenciaTotalUseCase,
)
from acutis_api.communication.requests.admin_doacoes import (
    CardDoacoesTotalResponse,
    CardMediaTotalResponse,
    CardRecorrentesComDoadoresResponse,
    CardsDoacoesRecorrentesResponse,
    ListarDoacoesQuery,
)
from acutis_api.communication.responses.admin_doacoes import (
    ListarDoacoesResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
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


@admin_doacoes_bp.put('/contabilizar-doacao/<uuid:fk_doacao_id>')
@swagger.validate(
    resp=Response(HTTP_200=ResponsePadraoSchema, HTTP_500=ErroPadraoResponse),
    tags=['Admin - Doações'],
)
@jwt_required()
def contabilizar_doacoes(fk_doacao_id):
    """Contabilizar doações"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = ContabilizarDoacoesUseCase(repository)
        response = usecase.execute(fk_doacao_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-total-do-dia')
@swagger.validate(
    resp=Response(
        HTTP_200=CardDoacoesTotalResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_total_do_dia():
    """Contabilizar doações"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = CardDoacoesDoDiaUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-total-do-mes')
@swagger.validate(
    resp=Response(
        HTTP_200=CardDoacoesTotalResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_total_do_mes():
    """Contabilizar doações"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = CardDoacoesDoMesUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-media-diaria')
@swagger.validate(
    resp=Response(
        HTTP_200=CardMediaTotalResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_media_diaria():
    """Média mensal doações"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = MediaDiariaUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-media-mensal')
@swagger.validate(
    resp=Response(
        HTTP_200=CardMediaTotalResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_media_mensal():
    """Média mensal doações"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = MediaMensalUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-recorrentes-nao-efetuadas')
@swagger.validate(
    resp=Response(
        HTTP_200=CardsDoacoesRecorrentesResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_recorrentes_nao_efetuadas():
    """Contabilizar doações recorrentes não efetuadas"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = RecorrenciaNaoEfetuadaUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-recorrentes-total')
@swagger.validate(
    resp=Response(
        HTTP_200=CardRecorrentesComDoadoresResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_recorrentes_total():
    """Contabilizar doações recorrentes total"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = RecorrenciaTotalUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-recorrentes-previstas')
@swagger.validate(
    resp=Response(
        HTTP_200=CardsDoacoesRecorrentesResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_recorrentes_previstas():
    """Contabilizar doações recorrentes previstas"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = RecorrenciasPrevistasUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-lembretes-efetivos')
@swagger.validate(
    resp=Response(
        HTTP_200=CardRecorrentesComDoadoresResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_lembretes_efetivos():
    """Contabilizar doações lembretes efetivos"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = RecorrenciasLembretesEfetivosUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-recorrentes-efetuadas')
@swagger.validate(
    resp=Response(
        HTTP_200=CardsDoacoesRecorrentesResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_recorrentes_efetuadas():
    """Contabilizar doações recorrentes efetuadas"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = RecorrenciasEfetuadasUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@admin_doacoes_bp.get('/card-recorrentes-canceladas')
@swagger.validate(
    resp=Response(
        HTTP_200=CardsDoacoesRecorrentesResponse, HTTP_500=ErroPadraoResponse
    ),
    tags=['Admin - Doações'],
)
@jwt_required()
def card_recorrentes_canceladas():
    """Contabilizar doações recorrentes canceladas"""
    try:
        repository = AdminDoacoesRepository(database)
        usecase = RecorrenciasCanceladasUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
