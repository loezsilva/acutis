from http import HTTPStatus

from flask import Blueprint
from spectree import Response

from acutis_api.application.use_cases.enderecos.buscar.buscar_cep import (
    BuscarCepUseCase,
)
from acutis_api.communication.responses.enderecos import BuscarCEPResponse
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.enderecos import (
    EnderecosRepository,
)

enderecos_bp = Blueprint('enderecos_bp', __name__, url_prefix='/enderecos')


@enderecos_bp.get('/buscar-cep/<cep>')
@swagger.validate(
    resp=Response(HTTP_200=BuscarCEPResponse), tags=['Endereços']
)
def buscar_cep(cep: str):
    """
    Busca os dados de endereço pelo CEP
    """
    try:
        repository = EnderecosRepository(database)
        usecase = BuscarCepUseCase(repository)

        response = usecase.execute(cep)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response
