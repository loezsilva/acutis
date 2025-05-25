import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import current_user, jwt_required
from spectree import Response

from acutis_api.application.use_cases.doacoes.atualizar import (
    CancelarRecorrenciaDoacaoUseCase,
    EstornarDoacaoCartaoCreditoUseCase,
)
from acutis_api.application.use_cases.doacoes.registrar import (
    RegistrarDoacaoBoletoUseCase,
    RegistrarDoacaoCartaoCreditoUseCase,
    RegistrarDoacaoPixUseCase,
)
from acutis_api.communication.requests.doacoes import (
    RegistrarDoacaoBoletoRequest,
    RegistrarDoacaoCartaoCreditoRequest,
    RegistrarDoacaoPixRequest,
)
from acutis_api.communication.responses.doacoes import (
    RegistrarDoacaoPixResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, limiter, swagger
from acutis_api.infrastructure.repositories.doacoes import DoacoesRepository
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.services.itau import ItauPixService
from acutis_api.infrastructure.services.maxipago import MaxiPago
from acutis_api.infrastructure.services.sendgrid import SendGridService

doacoes_bp = Blueprint('doacoes_bp', __name__, url_prefix='/doacoes')


@doacoes_bp.post('/pagamento/cartao-de-credito')
@swagger.validate(
    json=RegistrarDoacaoCartaoCreditoRequest,
    resp=Response(HTTP_201=ResponsePadraoSchema, HTTP_422=ErroPadraoResponse),
    tags=['Doações'],
)
@jwt_required()
@limiter.limit('1 per 5 seconds')
def efetuar_doacao_via_cartao_credito():
    """Realiza uma doação única ou recorrente via cartão de crédito"""
    try:
        request = RegistrarDoacaoCartaoCreditoRequest.model_validate(
            flask_request.json
        )

        repository = DoacoesRepository(database)
        maxipago = MaxiPago()
        file_service = file_service_factory()
        notification = SendGridService()
        usecase = RegistrarDoacaoCartaoCreditoUseCase(
            repository, maxipago, file_service, notification
        )
        usecase.execute(request, current_user)

        return {'msg': 'Doação realizada com sucesso.'}, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@doacoes_bp.post('/pagamento/cancelar-recorrencia/<uuid:doacao_id>')
@swagger.validate(
    resp=Response(HTTP_200=ResponsePadraoSchema),
    tags=['Doações'],
)
@jwt_required()
def cancelar_recorrencia_doacao(doacao_id: uuid.UUID):
    """Cancela a recorrencia da doação pelo ID da doação"""
    try:
        repository = DoacoesRepository(database)
        maxipago = MaxiPago()
        usecase = CancelarRecorrenciaDoacaoUseCase(repository, maxipago)
        usecase.execute(doacao_id, current_user)

        return {'msg': 'Doação recorrente cancelada com sucesso.'}
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@doacoes_bp.post(
    '/pagamento/cartao-de-credito/estornar/<uuid:processamento_doacao_id>'
)
@swagger.validate(
    resp=Response(HTTP_200=ResponsePadraoSchema), tags=['Doações']
)
@jwt_required()
def estornar_doacao_cartao_credito(processamento_doacao_id: uuid.UUID):
    """Realiza o estorno da doação via cartão de crédito pelo ID"""
    try:
        repository = DoacoesRepository(database)
        maxipago = MaxiPago()
        usecase = EstornarDoacaoCartaoCreditoUseCase(repository, maxipago)
        usecase.execute(processamento_doacao_id, current_user)

        return {'msg': 'O estorno do valor foi efetuado com sucesso.'}
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@doacoes_bp.post('/pagamento/pix')
@swagger.validate(
    json=RegistrarDoacaoPixRequest,
    resp=Response(
        HTTP_201=RegistrarDoacaoPixResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Doações'],
)
@jwt_required()
def efetuar_doacao_via_pix():
    """Realiza uma doação via pix"""
    try:
        request = RegistrarDoacaoPixRequest.model_validate(flask_request.json)

        repository = DoacoesRepository(database)
        itau = ItauPixService()
        file_service = file_service_factory()
        usecase = RegistrarDoacaoPixUseCase(repository, itau, file_service)

        response = usecase.execute(request, current_user)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@doacoes_bp.post('/pagamento/boleto')
@swagger.validate(
    json=RegistrarDoacaoBoletoRequest,
    resp=Response(HTTP_201=None, HTTP_422=ErroPadraoResponse),
    tags=['Doações'],
)
@jwt_required()
def efetuar_doacao_via_boleto():
    """Realiza uma doação via boleto"""
    try:
        request = RegistrarDoacaoBoletoRequest.model_validate(
            flask_request.json
        )

        repository = DoacoesRepository(database)
        itau = ItauPixService()
        file_service = file_service_factory()
        usecase = RegistrarDoacaoBoletoUseCase(repository, itau, file_service)

        response = usecase.execute(request, current_user)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response
