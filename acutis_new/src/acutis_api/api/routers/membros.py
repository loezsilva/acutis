from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from spectree import Response

from acutis_api.application.use_cases.membros import (
    RegistrarNovoLeadUseCase,
    RegistrarNovoMembroUseCase,
)
from acutis_api.communication.requests.membros import (
    RegistrarNovoLeadRequest,
    RegistrarNovoMembroFormData,
)
from acutis_api.communication.responses.membros import (
    RegistrarNovoLeadResponse,
    RegistrarNovoMembroResponse,
)
from acutis_api.communication.responses.padrao import ErroPadraoResponse
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
