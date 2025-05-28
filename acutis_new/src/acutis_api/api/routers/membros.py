import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import current_user, get_current_user, jwt_required
from spectree import Response

from acutis_api.application.use_cases.membros import (
    AtualizarDadosMembroUseCase,
    AtualizarFotoMembroUseCase,
    RegistrarNovoLeadUseCase,
    RegistrarNovoMembroUseCase,
)
from acutis_api.application.use_cases.membros.buscar import (
    BuscarCardDoacoesMembroBenfeitorUseCase,
    BuscarHistoricoDoacaoUseCase,
)
from acutis_api.application.use_cases.membros.deletar import (
    ConfirmaExclusaoContaUseCase,
)
from acutis_api.application.use_cases.membros.deletar.excluir_conta import (
    ExcluirContaUseCase,
)
from acutis_api.application.use_cases.membros.listar import (
    ListarDoacoesUseCase,
)
from acutis_api.communication.requests.autenticacao import (
    VerificarTokenRequest,
)
from acutis_api.communication.requests.membros import (
    AtualizarDadosMembroRequest,
    AtualizarFotoMembroFormData,
    RegistrarNovoLeadRequest,
    RegistrarNovoMembroFormData,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.communication.responses.membros import (
    CardDoacoesMembroBenfeitorResponse,
    DoacoesMembroBenfeitorResponse,
    HistoricoDoacaoResponse,
    RegistrarNovoLeadResponse,
    RegistrarNovoMembroResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.membros import (
    MembrosRepository,
)
from acutis_api.infrastructure.services.factories import (
    file_service_factory,
)
from acutis_api.infrastructure.services.sendgrid import SendGridService

membros_bp = Blueprint('membros_bp', __name__, url_prefix='/membros')


@membros_bp.post('/registrar-novo-membro')
@swagger.validate(
    form=RegistrarNovoMembroFormData,
    resp=Response(
        HTTP_201=RegistrarNovoMembroResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Membros'],
)
def registrar_novo_membro():
    """
    Registra um novo membro
    """
    try:
        request = RegistrarNovoMembroFormData(
            membro=flask_request.form['membro'],
            endereco=flask_request.form['endereco'],
            foto=flask_request.files.get('foto'),
            campanha_id=flask_request.form.get('campanha_id'),
        )

        repository = MembrosRepository(database)
        file_service = file_service_factory()
        notification = SendGridService()
        usecase = RegistrarNovoMembroUseCase(
            repository, file_service, notification
        )

        response = usecase.execute(request)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@membros_bp.post('/registrar-novo-lead')
@swagger.validate(
    json=RegistrarNovoLeadRequest,
    resp=Response(
        HTTP_201=RegistrarNovoLeadResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Membros'],
)
def registrar_novo_lead():
    """
    Registra um novo lead
    """
    try:
        request = RegistrarNovoLeadRequest.model_validate(flask_request.json)

        repository = MembrosRepository(database)
        file_service = file_service_factory()
        notification = SendGridService()
        usecase = RegistrarNovoLeadUseCase(
            repository, file_service, notification
        )

        response = usecase.execute(request)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@membros_bp.get('/excluir-conta')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Membros'],
)
@jwt_required()
def excluir_conta():
    """
    Envia email para confirmar exclusão de conta.
    """
    try:
        notification = SendGridService()
        usecase = ExcluirContaUseCase(notification)
        usecase.execute()
        return {
            'msg': 'Verifique sua solicitação de exclusão em seu e-mail.',
        }, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@membros_bp.delete('/confirma-exclusao-de-conta')
@swagger.validate(
    json=VerificarTokenRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Membros'],
)
def confirma_exclusao_de_conta():
    """
    Confirma e realiza exclusão de conta.
    """
    try:
        request = VerificarTokenRequest.model_validate(
            flask_request.get_json()
        )
        repository = MembrosRepository(database)
        usecase = ConfirmaExclusaoContaUseCase(repository)
        usecase.execute(request)
        return {
            'msg': 'Conta excluída com sucesso.',
        }, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@membros_bp.get('/listar-doacoes')
@swagger.validate(
    query=PaginacaoQuery,
    resp=Response(
        HTTP_200=DoacoesMembroBenfeitorResponse,
    ),
    tags=['Membros - Benfeitores'],
)
@jwt_required()
def listar_doacoes():
    """Lista todas as doações identificadas do usuário"""
    try:
        filtros = PaginacaoQuery.model_validate(flask_request.args.to_dict())

        repository = MembrosRepository(database)
        file_service = file_service_factory()
        usecase = ListarDoacoesUseCase(repository, file_service)

        response = usecase.execute(filtros, current_user)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@membros_bp.get('/buscar-historico-doacao/<uuid:doacao_id>')
@swagger.validate(
    query=PaginacaoQuery,
    resp=Response(HTTP_200=HistoricoDoacaoResponse),
    tags=['Membros - Benfeitores'],
)
@jwt_required()
def buscar_historico_doacao(doacao_id: uuid.UUID):
    """Busca o historico da doação pelo ID da doação."""
    try:
        filtros = PaginacaoQuery.model_validate(flask_request.args.to_dict())

        repository = MembrosRepository(database)
        usecase = BuscarHistoricoDoacaoUseCase(repository)

        response = usecase.execute(filtros, current_user, doacao_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@membros_bp.put('/atualizar-dados-membro')
@swagger.validate(
    json=AtualizarDadosMembroRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_422=ErroPadraoResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Membros'],
)
@jwt_required()
def atualizar_dados_membro():
    """
    Atualiza os dados de um membro, buscando através do id do lead
    """
    try:
        usuario_logado = get_current_user()

        request = AtualizarDadosMembroRequest.model_validate(
            flask_request.json
        )

        repository = MembrosRepository(database)
        usecase = AtualizarDadosMembroUseCase(repository)

        response = usecase.execute(request, usuario_logado)

        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@membros_bp.put('/atualizar-foto-membro')
@swagger.validate(
    form=AtualizarFotoMembroFormData,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Membros'],
)
@jwt_required()
def atualizar_foto_membro():
    """
    Atualiza a foto de um membro, buscando através do id do lead
    """
    try:
        usuario_logado = get_current_user()

        request = AtualizarFotoMembroFormData(
            foto=flask_request.files.get('foto'),
        )

        repository = MembrosRepository(database)
        file_service = file_service_factory()
        usecase = AtualizarFotoMembroUseCase(repository, file_service)

        response = usecase.execute(request, usuario_logado)
        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@membros_bp.get('/buscar-card-doacoes')
@swagger.validate(
    resp=Response(HTTP_200=CardDoacoesMembroBenfeitorResponse),
    tags=['Membros - Benfeitores'],
)
@jwt_required()
def buscar_card_doacoes():
    """Retorna o card de doações do membro benfeitor logado"""
    try:
        repository = MembrosRepository(database)
        usecase = BuscarCardDoacoesMembroBenfeitorUseCase(repository)

        response = usecase.execute(current_user)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
