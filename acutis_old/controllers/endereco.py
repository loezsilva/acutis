from builder import db
import json
from flask_jwt_extended import jwt_required, current_user
from spectree import Response
from flask import Blueprint
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.errors_handler import errors_handler
from handlers.addresses.put.atualiza_endereco_via_telefone import (
    AtualizarEnderecoViaTelefoneUseCase,
)
from models.schemas.endereco.atualizar_endereco_por_telefone import (
    AtualizarEnderecoPorTelefoneRequest,
)
from utils.response import DefaultErrorResponseSchema, response_handler
from models.endereco import (
    AddressResponseSchema,
    AtualizarEnderecoPorUserIdResponse,
    Endereco,
)
from builder import api
from flask import request as flask_request

address_controller = Blueprint("address_controller", __name__, url_prefix="/addresses")


@address_controller.get("/me")
@api.validate(
    resp=Response(
        HTTP_200=AddressResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Endereços"],
)
@jwt_required()
def get_address_by_logged_user():
    """
    Retorna o endereço do usuário logado.
    """
    try:
        address = Endereco.query.filter_by(
            fk_clifor_id=current_user["fk_clifor_id"]
        ).first()
        if not address:
            raise NotFoundError("Endereço não encontrado.")

        response = AddressResponseSchema.from_orm(address).json()

        return json.loads(response), 200

    except Exception as err:
        response_error = errors_handler(err)
        return response_error


@address_controller.put("/atualizar-por-telefone")
@api.validate(
    json=AtualizarEnderecoPorTelefoneRequest,
    resp=Response(
        HTTP_200=AtualizarEnderecoPorUserIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Endereços"],
)
@jwt_required()
def atualiza_endereco_por_user_id():
    try:
        request = AtualizarEnderecoPorTelefoneRequest.parse_obj(
            flask_request.get_json()
        )
        usecase = AtualizarEnderecoViaTelefoneUseCase(db)
        response = usecase.execute(request)
        return response_handler(response)
    except Exception as exc:
        db.session.rollback()
        return errors_handler(exc)
