from handlers.gateway.update.update_gateway import UpdateGateway
from datetime import datetime
import logging
from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint
from flask.globals import request
from spectree import Response
from exceptions.errors_handler import errors_handler
from handlers.gateway.create.create_gateway import CreateGateway
from handlers.gateway.get.gateway_by_id import GetGatewayByID
from handlers.gateway.get.gateway_get_all import GatewayGetAll
from utils.verify_permission import permission_required
from models.gateway_pagamento import (
    PaymentGatewayCreateSchema,
    PaymentGatewayResponseSchema,
    UpdatePaymentSetup,
)
from utils.response import (
    DefaultResponseSchema,
    DefaultErrorResponseSchema,
    response_handler,
)
from models import GatewayPagamento, SetupPagamento
from builder import db, api


payment_gateway_controller = Blueprint(
    "payment_gateway_controller", __name__, url_prefix="/payments-gateway"
)


OPTIONAL_FIELDS_LIST = ["status", "merchant_id", "merchant_key"]


@payment_gateway_controller.post("")
@api.validate(
    json=PaymentGatewayCreateSchema,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Gateway de pagamentos"],
)
@jwt_required()
@permission_required("gateway", "criar")
def create_payment_gateway():
    """
    Cria um novo gateway de pagamento
    """
    try:
        create = CreateGateway(db)
        response = response_handler(create.execute(), save_logs=False)
        return response

    except Exception as e:
        response_error = errors_handler(e, save_logs=False)
        return response_error


@payment_gateway_controller.put("/<int:payment_gateway_id>")
@api.validate(
    json=PaymentGatewayCreateSchema,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Gateway de pagamentos"],
)
@jwt_required()
@permission_required("gateway", "editar")
def update_payment_gateway(payment_gateway_id):
    """
    Atualiza o registro de um gateway de pagamento pelo ID
    """

    try:
        update_gateway = UpdateGateway(db, payment_gateway_id)
        response = response_handler(update_gateway.execute(), save_logs=True)
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error


@payment_gateway_controller.delete("/<int:payment_gateway_id>")
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Gateway de pagamentos"],
)
@jwt_required()
@permission_required("gateway", "deletar")
def delete_payment_gateway(payment_gateway_id):
    """
    Deleta o registro de um gateway de pagamento pelo ID
    """
    payment_gateway = db.session.get(GatewayPagamento, payment_gateway_id)
    if not payment_gateway:
        return {
            "error": f"Gateway de pagamento com id {payment_gateway_id} não encontrado."
        }, 404

    db.session.delete(payment_gateway)

    try:
        db.session.commit()
    except Exception as err:
        logging.error(f"{type(err)} - {err}")
        db.session.rollback()
        return {
            "error": "Ocorreu um erro ao deletar o registro do gateway de pagamento."
        }, 500

    return {"msg": "Gateway de pagamento deletado com sucesso."}, 200


@payment_gateway_controller.get("/<int:payment_gateway_id>")
@api.validate(
    resp=Response(
        HTTP_200=PaymentGatewayResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Gateway de pagamentos"],
)
@jwt_required()
def get_payment_gateway(payment_gateway_id):
    """
    Retorna o registro de uma gateway de pagamento pelo ID
    """
    try:
        get_gateway = GetGatewayByID(payment_gateway_id, db)
        response = response_handler(get_gateway.execute(), save_logs=True)
        return response
    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        return response_error


@payment_gateway_controller.get("")
@api.validate(
    resp=Response(
        HTTP_200=PaymentGatewayResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Gateway de pagamentos"],
)
@jwt_required()
@permission_required("campanha", "criar")
def get_payments_gateways():
    """
    Retorna todos os gateways de pagamentos registrados
    """
    try:
        get_all = GatewayGetAll()
        response = response_handler(get_all.execute(), save_logs=True)
        return response
    except Exception as e:
        error_response = errors_handler(e, save_logs=True)
        return error_response


@payment_gateway_controller.put("/payment-setup")
@api.validate(
    json=UpdatePaymentSetup,
    resp=Response(HTTP_200=None, HTTP_403=None, HTTP_500=None),
    tags=["Gateway de pagamentos"],
)
@jwt_required()
@permission_required("gateway", "editar")
def update_setup_payment():
    """Atualiza o setup de pagamento de cartão, pix e boleto"""
    try:

        data = request.get_json()

        credito_unico = data["credito_unico"]
        credito_recorrente = data["credito_recorrente"]
        pix_unico = data["pix_unico"]
        pix_recorrente = data["pix_recorrente"]
        boleto_unico = data["boleto_unico"]
        boleto_recorrente = data["boleto_recorrente"]

        setup = SetupPagamento.query.first()

        gateways = set(
            db.session.execute(db.select(GatewayPagamento.id)).scalars().all()
        )

        ids_validos = {
            credito_unico,
            credito_recorrente,
            pix_unico,
            pix_recorrente,
            boleto_unico,
            boleto_recorrente,
        }

        if not ids_validos.issubset(gateways):
            id_invalido = next(
                (id for id in ids_validos if id not in gateways), None
            )
            return {
                "error": f"O gateway de pagamento com id {id_invalido} não existe."
            }, 404

        setup.credito_unico = credito_unico
        setup.credito_recorrente = credito_recorrente
        setup.pix_unico = pix_unico
        setup.pix_recorrente = pix_recorrente
        setup.boleto_unico = boleto_unico
        setup.boleto_recorrente = boleto_recorrente
        setup.data_alteracao = datetime.now()
        setup.usuario_alteracao = current_user["id"]

        db.session.commit()

        return {"msg": "Setup de pagamento atualizado com sucesso."}, 200

    except Exception as exception:
        db.session.rollback()
        return {
            "error": "Ocorreu um erro ao atualizar as opções de pagamentos.",
            "exception": str(exception),
        }, 500
