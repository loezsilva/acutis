from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from spectree import Response

from acutis_api.application.use_cases.membros_oficiais import (
    RegistrarNovoMembroOficialUseCase,
)
from acutis_api.communication.requests.membros_oficiais import (
    RegistrarMembroOficialRequest,
)
from acutis_api.communication.responses.membros_oficiais import (
    RegistrarNovoMembroOficialResponse,
)
from acutis_api.communication.responses.padrao import ErroPadraoResponse
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.membros_oficiais import (
    MembrosOficiaisRepository,
)
from acutis_api.infrastructure.services.sendgrid import SendGridService

membros_oficiais_bp = Blueprint(
    'membros_oficiais_bp', __name__, url_prefix='/membros-oficiais'
)


@membros_oficiais_bp.post('/registrar')
@swagger.validate(
    json=RegistrarMembroOficialRequest,
    resp=Response(
        HTTP_200=RegistrarNovoMembroOficialResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Cargos Oficiais'],
)
def registrar_novo_membro_oficial():
    """
    Registra novo membro oficial
    """
    try:
        request = RegistrarMembroOficialRequest.model_validate(
            flask_request.get_json()
        )
        repository = MembrosOficiaisRepository(database)
        notification = SendGridService()
        usecase = RegistrarNovoMembroOficialUseCase(repository, notification)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)
