import controllers
from handlers.checkout.get.export_donations_not_paid import (
    ExportRecurrencesNotPaid,
)
from handlers.checkout.get.export_donations_recurrences_made import (
    ExportDonationsRecurrencesMade,
)
from handlers.checkout.get.card_recurrence_planned import (
    CardRecurrencePlanned,
)
from handlers.checkout.get.export_recurrences_planneds import (
    ExportRecurrencesPlanned,
)
from handlers.checkout.get.exportar_doacoes import ExportarDoacoes
from handlers.checkout.get.exportar_recorretes_em_lapso import ExportarDoacoesEmLapsos
from handlers.checkout.get.get_donors_ranking import GetDonorsRanking
from handlers.checkout.get.get_regular_donors import GetRegularDonors
from handlers.checkout.get.get_top_regular_donors import GetTopRegularDonors
from handlers.checkout.get.listar_todas_doacoes import ListaTodasDoacoes
from handlers.checkout.get.listing_doacoes_inadimplentes import (
    ListingDoacoesInadimplentes,
)
from handlers.checkout.get.listing_donations_planned import (
    DonationsPlanned,
)
from models.schemas.checkout.get.exportar_doacoes_schema import ExportarDoacoesResponse, ExportarRecorrenciasAtivasRequest
from models.schemas.checkout.get.get_donors_ranking import (
    GetDonorsRankingQueryFilter,
    GetDonorsRankingResponse,
)
from models.schemas.checkout.get.get_regular_donors import (
    GetRegularDonorsQueryFilter,
    GetRegularDonorsResponse,
)
from models.schemas.checkout.get.listar_doacoes_schema import ListarDoacoesQuery, ListarDoacoesResponse
from models.schemas.checkout.get.listar_recorrencias_canceladas import ListarRecorrenciasCanceladasQuery
from models.schemas.checkout.post.send_reminder_unpaid_donation import (
    SendReminderUnpaidDonationRequest,
)
from models.schemas.checkout.schema_card_recurrence_planned import (
    ReponseCardRecurrencePlanned,
)
from models.schemas.checkout.schema_list_donations_exception import (
    ResponseDonationsExceptions,
)
from models.schemas.checkout.schema_list_donations_planned import (
    ResponsePlanned,
)
from models.schemas.checkout.get.get_top_regular_donors import (
    GetTopRegularDonorsQueryFilter,
    GetTopRegularDonorsResponse,
)
from models.schemas.checkout.schema_recurrence_not_paid import ListagemDeRecorreciaEmLapsosRequest
import repositories
from repositories.checkout_repository import CheckoutRepository
from services.factories import file_service_factory
from utils.response import DefaultResponseSchema, response_handler
from handlers.checkout.get.listing_exeception_donations import (
    ListingExceptionDonations,
)
from handlers.checkout.get.listing_recurrence_not_paid import (
    ListingRecurrenceNotPaid,
)
from handlers.checkout.get.add_user_except_donations import (
    AddUserExceptDonations,
)
from handlers.checkout.get.card_recurrence_donations import (
    CardRecurrenceDonations,
)
from handlers.checkout.get.listar_doacoes_canceladas import (
    ListarRecorrenciasCanceladas,
)
from models.schemas.checkout.listar_recorrencias_canceladas_schema import (
    ListarRecorrenciasCanceladasResponse
)
from handlers.checkout.get.include_donations import IncludeDonations
from handlers.checkout.get.list_donations_not_contabilizaded import (
    DonationsNotContabilizaded,
)
from models.schemas.checkout.validator_list_recurrence_made import (
    ResponseDonationsRecurrenceMade,
)
import logging
import os
from exceptions.errors_handler import errors_handler
from handlers.checkout.send_reminder_unpaid_donation import (
    SendReminderUnpaidDonation,
)
from utils.export_donations_desconsideradas import (
    ExportDonationsDesconsideradas,
)
from utils.export_donations_canceladas import ExportDonationsCanceladas
from handlers.checkout.get.list_transaction_by_id import (
    ListTransactionById,
)
from models.schemas.checkout.validator_list_transaction import (
    ResponseListTransaction,
)

from flask_jwt_extended import (
    jwt_required,
    current_user,
)

from itsdangerous import BadSignature, BadTimeSignature, SignatureExpired
from utils.verify_permission import permission_required
from flask import Blueprint, jsonify
from flask.globals import request
from spectree import Response
from templates.email_templates import (
    recurrence_pix_invoice_payment_email_template,
)

from handlers.payments.credit_card.reverse_credit_card_payment import (
    ReverseCreditCardPayment,
)

from handlers.payments.cancel_pix_invoice_recurrence_payment import (
    CancelPixInvoiceRecurrencePayment,
)
from handlers.payments.credit_card.create_recurrence_payment import (
    CreateCreditCardRecurrencePayment,
)
from handlers.payments.credit_card.cancel_recurrence_payment import (
    CancelCreditCardRecurrencePayment,
)
from handlers.payments.credit_card.create_payment import (
    CreateCreditCardPayment,
)
from handlers.payments.invoice.create_new_recurrence_payment import (
    CreateNewInvoiceRecurrencePayment,
)
from handlers.payments.invoice.create_payment import CreateInvoicePayment
from handlers.payments.invoice.get_payment import GetInvoicePayment
from handlers.payments.pix.create_new_recurrence_payment import (
    CreateNewPixRecurrencePayment,
)
from handlers.payments.pix.create_payment import CreatePixPayment
from handlers.payments.pix.get_payment import GetPixPayment
from handlers.payments.resend_email_pix_invoice_payment import (
    ResendEmailPixInvoicePayment,
)
from models.setup_pagamento import SetupPagamento
from utils.checkout import (
    CheckoutCreditCardSchema,
    CheckoutDonationsQuerySchema,
    InvoiceTransactionSchema,
    PixCreateSchema,
)
from models import (
    Usuario,
    Clifor,
    Campanha,
    Pedido,
    ProcessamentoPedido,
)
from utils.response import DefaultErrorResponseSchema
from utils.token_email import generate_token, verify_token
from utils.send_email import send_email
from builder import db, api, limiter
from utils.logs_access import log_access
from handlers.checkout.get.list_donations_recurrence_made import (
    RecurrenceDonationsMade,
)

checkout_controller = Blueprint(
    "checkout_controller", __name__, url_prefix="/checkout"
)


OPTIONAL_FIELDS_LIST = [
    "fk_campanha_id",
    "fk_landpage_id",
    "data_nascimento",
    "sexo",
    "telefone",
    "complemento",
    "cargo_id",
    "usuario_superior_id",
    "avatar",
    "numero",
    "bairro",
    "cidade",
    "estado",
    "cep",
    "rua",
]


@checkout_controller.post("/payment/credit-card")
@api.validate(
    json=CheckoutCreditCardSchema,
    resp=Response(HTTP_201=None, HTTP_400=None, HTTP_500=None),
    tags=["Checkout"],
)
@jwt_required()
@limiter.limit("1 per 5 seconds")
def checkout_credit_card_payment():
    """
    Pagamento único com cartão de crédito pelo Gateway ativo no sistema
    """
    try:
        fk_campanha_id = request.get_json()["fk_campanha_id"]
    except KeyError as key_error:
        return {"error": f"O campo {key_error} é obrigatório."}, 400

    payment_setup = SetupPagamento.query.filter_by(
        fk_campanha_id=fk_campanha_id
    ).first()
    if payment_setup is None:
        return {
            "error": "O setup de pagamento para esta campanha não foi encontrado."
        }, 404

    credit_card = CreateCreditCardPayment(payment_setup.credito_unico)

    return credit_card.execute()


@checkout_controller.post("/payment/credit-card/recurrence")
@api.validate(
    json=CheckoutCreditCardSchema,
    resp=Response(HTTP_201=None, HTTP_400=None, HTTP_500=None),
    tags=["Checkout"],
)
@jwt_required()
@limiter.limit("1 per 5 seconds")
def checkout_credit_card_recurrence_payment():
    """
    Pagamento recorrente com cartão de crédito pelo Gateway ativo no sistema
    """
    try:
        fk_campanha_id = request.get_json()["fk_campanha_id"]
    except KeyError as key_error:
        return {"error": f"O campo {key_error} é obrigatório."}, 400

    payment_setup = SetupPagamento.query.filter_by(
        fk_campanha_id=fk_campanha_id
    ).first()
    if payment_setup is None:
        return {
            "error": "O setup de pagamento para esta campanha não foi encontrado."
        }, 404

    credit_card = CreateCreditCardRecurrencePayment(
        payment_setup.credito_recorrente
    )

    return credit_card.execute()


@checkout_controller.post("/payment/cancel-recurrence/<int:fk_pedido_id>")
@api.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_400=None,
        HTTP_404=None,
        HTTP_409=None,
        HTTP_500=None,
    ),
    tags=["Checkout"],
)
@jwt_required()
def checkout_cancel_recurrence_payment(fk_pedido_id: int):
    """
    Cancela a recorrencia de pagamento pelo ID do pedido
    """
    permission_donation = current_user["permissoes"]["doacoes"]["editar"] == 1

    if (pedido := db.session.get(Pedido, fk_pedido_id)) is None:
        return {"error": "Pedido não encontrado."}, 404

    if (
        not permission_donation
        and pedido.fk_clifor_id != current_user["fk_clifor_id"]
    ):
        return {
            "error": "Você não tem permissão para cancelar esta doação."
        }, 403

    if pedido.fk_forma_pagamento_id == 1:
        credit_card = CancelCreditCardRecurrencePayment(pedido)

        return credit_card.execute()

    pix_invoice = CancelPixInvoiceRecurrencePayment(pedido)

    return pix_invoice.execute()


@checkout_controller.post("/payment/credit-card/reversal/<int:fk_pedido_id>")
@api.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_400=None,
        HTTP_403=None,
        HTTP_404=None,
        HTTP_500=None,
    ),
    tags=["Checkout"],
)
@jwt_required()
@permission_required("doacoes", "editar")
def reverse_user_credit_card_payment(fk_pedido_id: int):
    """
    Realiza o estorno do pagamento via cartão de credito pelo ID do pedido
    """

    if (pedido := db.session.get(Pedido, fk_pedido_id)) is None:
        return {"error": "Doação não encontrada."}, 404

    credit_card = ReverseCreditCardPayment(pedido)

    return credit_card.execute()


@checkout_controller.post("/payment/pix")
@api.validate(
    json=PixCreateSchema,
    resp=Response(HTTP_201=None, HTTP_400=None, HTTP_500=None),
    tags=["Checkout"],
)
@jwt_required()
@limiter.limit("1 per 5 seconds")
def checkout_pix_payment():
    """
    Pagamento único ou recorrente com PIX pelo Gateway ativo no sistema
    """
    try:
        periodicidade = request.get_json()["periodicidade"]
        fk_campanha_id = request.get_json()["fk_campanha_id"]
    except KeyError as exception:
        return {"error": f"O campo {exception} é obrigatório."}, 400

    payment_setup = SetupPagamento.query.filter_by(
        fk_campanha_id=fk_campanha_id
    ).first()
    if payment_setup is None:
        return {
            "error": "O setup de pagamento para esta campanha não foi encontrado."
        }, 404

    payment_setup_map = {
        1: payment_setup.pix_unico,
        2: payment_setup.pix_recorrente,
    }

    pix = CreatePixPayment(payment_setup_map[periodicidade])

    return pix.execute()


@checkout_controller.post("/payment/invoice")
@api.validate(
    json=InvoiceTransactionSchema,
    resp=Response(HTTP_201=None, HTTP_400=None, HTTP_404=None, HTTP_500=None),
    tags=["Checkout"],
)
@jwt_required()
@limiter.limit("1 per 5 seconds")
def checkout_invoice_payment():
    """
    Pagamento único ou recorrente com boleto pelo Gateway ativo no sistema
    """
    try:
        periodicidade = request.get_json()["periodicidade"]
        fk_campanha_id = request.get_json()["fk_campanha_id"]
    except KeyError as exception:
        return {"error": f"O campo {exception} é obrigatório."}, 400

    payment_setup = SetupPagamento.query.filter_by(
        fk_campanha_id=fk_campanha_id
    ).first()
    if payment_setup is None:
        return {
            "error": "O setup de pagamento para esta campanha não foi encontrado."
        }, 404

    payment_setup_map = {
        1: payment_setup.boleto_unico,
        2: payment_setup.boleto_recorrente,
    }

    invoice = CreateInvoicePayment(payment_setup_map[periodicidade])

    return invoice.execute()


@checkout_controller.post("/payment/resend-email")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_403=None, HTTP_404=None, HTTP_500=None),
    tags=["Checkout"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def resend_email_pix_invoice_payment():
    """
    Reenvia o link de pagamento pix ou boleto para o email do usuário
    """

    try:
        body = request.get_json()

        transaction_id = body.get("transaction_id", None)
        if not transaction_id:
            fk_processamento_pedido_id = body["fk_processamento_pedido_id"]

            s3_client = file_service_factory()
            bucket_name = os.environ.get("NAME_BUCKET")

            pedido = (
                db.session.query(
                    Usuario.id.label("fk_usuario_id"),
                    Usuario.nome.label("usuario_nome"),
                    Usuario.email.label("usuario_email"),
                    ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
                    Pedido.id.label("fk_pedido_id"),
                    Pedido.fk_campanha_id,
                    Pedido.fk_gateway_pagamento_id,
                    Pedido.fk_forma_pagamento_id,
                    Campanha.titulo.label("nome_campanha"),
                    Campanha.filename.label("foto_campanha"),
                )
                .select_from(ProcessamentoPedido)
                .join(Clifor, Clifor.id == ProcessamentoPedido.fk_clifor_id)
                .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
                .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
                .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
                .filter(ProcessamentoPedido.id == fk_processamento_pedido_id)
                .first()
            )

            if pedido is None:
                return {"error": "Pedido não encontrado."}, 404

            foto_campanha = s3_client.get_public_url(pedido.foto_campanha)

            PAYMENT_TYPE_MAP = {
                2: {
                    "payment_type": "pix",
                    "payment_salt": "send_email_pix_recurrence_payment",
                },
                3: {
                    "payment_type": "invoice",
                    "payment_salt": "send_email_invoice_recurrence_payment",
                },
            }

            payment_type = PAYMENT_TYPE_MAP[pedido.fk_forma_pagamento_id]

            obj_user = {
                "id": pedido.fk_usuario_id,
                "fk_processamento_pedido_id": pedido.fk_processamento_pedido_id,
                "fk_pedido_id": pedido.fk_pedido_id,
                "fk_gateway_pagamento_id": pedido.fk_gateway_pagamento_id,
            }

            token = generate_token(
                obj=obj_user, salt=payment_type.get("payment_salt")
            )

            html = recurrence_pix_invoice_payment_email_template(
                name=pedido.usuario_nome,
                token=token,
                campanha_id=pedido.fk_campanha_id,
                nome_campanha=pedido.nome_campanha,
                tipo_pagamento=payment_type.get("payment_type"),
                foto_campanha=foto_campanha,
            )

            send_email("HeSed - Doação mensal", pedido.usuario_email, html, 3)

            response = {
                "msg": "Pedido de pagamento reenviado com sucesso."
            }, 200

            log_access(
                str(response),
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
                200,
            )

            return response, 200

    except KeyError as err:
        return {"error": f"O campo {err} é obrigatório."}, 400

    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        print(f"{str(type(err))} - {str(err)}")
        return {
            "error": "Ocorreu um erro ao reenviar o pedido de pagamento."
        }, 500

    pedido = (
        db.session.query(ProcessamentoPedido)
        .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
        .filter(ProcessamentoPedido.transaction_id == transaction_id)
        .with_entities(
            Pedido.fk_gateway_pagamento_id, Pedido.fk_forma_pagamento_id
        )
        .first()
    )

    if pedido is None:
        return {"error": "Pedido não encontrado."}, 404

    resend_payment = ResendEmailPixInvoicePayment(
        transaction_id=transaction_id,
        fk_gateway_pagamento_id=pedido.fk_gateway_pagamento_id,
        fk_forma_pagamento_id=pedido.fk_forma_pagamento_id,
    )

    return resend_payment.execute()


@checkout_controller.post("/payment/pix/recurrence/<token>")
@api.validate(
    resp=Response(HTTP_403=None, HTTP_404=None, HTTP_500=None),
    security={},
    tags=["Checkout"],
)
@limiter.limit("1 per 5 seconds")
def pix_recurrence_payment(token: str):
    """
    Gera o pagamento recorrente via pix pelo token
    """
    try:
        VALIDATE_TOKEN = 24 * 60 * 60 * 7

        payload = verify_token(
            token,
            salt="send_email_pix_recurrence_payment",
            max_age=VALIDATE_TOKEN,
        )

        fk_gateway_pagamento_id = payload["fk_gateway_pagamento_id"]

        if transaction_id := payload.get("transaction_id"):
            resend_payment = GetPixPayment(
                transaction_id=transaction_id,
                fk_gateway_pagamento_id=fk_gateway_pagamento_id,
            )

            return resend_payment.execute()

        VALIDATE_TOKEN = 24 * 60 * 60 * 30

        payload = verify_token(
            token,
            salt="send_email_pix_recurrence_payment",
            max_age=VALIDATE_TOKEN,
        )

        fk_usuario_id = payload["id"]
        fk_processamento_pedido_id = payload["fk_processamento_pedido_id"]
        fk_pedido_id = payload["fk_pedido_id"]

        new_payment = CreateNewPixRecurrencePayment(
            fk_usuario_id=fk_usuario_id,
            fk_processamento_pedido_id=fk_processamento_pedido_id,
            fk_pedido_id=fk_pedido_id,
            fk_gateway_pagamento_id=fk_gateway_pagamento_id,
        )

        return new_payment.execute()

    except SignatureExpired:
        return {"error": "Token expirado."}, 401

    except BadTimeSignature:
        return {"error": "Token inválido."}, 401

    except BadSignature:
        return {"error": "Token inválido."}, 401

    except Exception as exception:
        logging.error(exception)
        return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500


@checkout_controller.post("/payment/invoice/recurrence/<token>")
@api.validate(resp=Response(HTTP_500=None), security={}, tags=["Checkout"])
@limiter.limit("1 per 5 seconds")
def invoice_recurrence_payment(token: str):
    """
    Gera o pagamento recorrente via boleto pelo token
    """
    try:
        VALIDATE_TOKEN = 24 * 60 * 60 * 7

        payload = verify_token(
            token,
            salt="send_email_invoice_recurrence_payment",
            max_age=VALIDATE_TOKEN,
        )

        fk_gateway_pagamento_id = payload["fk_gateway_pagamento_id"]

        if transaction_id := payload.get("transaction_id"):
            resend_payment = GetInvoicePayment(
                transaction_id=transaction_id,
                fk_gateway_pagamento_id=fk_gateway_pagamento_id,
            )

            return resend_payment.execute()

        VALIDATE_TOKEN = 24 * 60 * 60 * 30

        payload = verify_token(
            token,
            salt="send_email_invoice_recurrence_payment",
            max_age=VALIDATE_TOKEN,
        )

        fk_usuario_id = payload["id"]
        fk_processamento_pedido_id = payload["fk_processamento_pedido_id"]
        fk_pedido_id = payload["fk_pedido_id"]

        new_payment = CreateNewInvoiceRecurrencePayment(
            fk_usuario_id=fk_usuario_id,
            fk_processamento_pedido_id=fk_processamento_pedido_id,
            fk_pedido_id=fk_pedido_id,
            fk_gateway_pagamento_id=fk_gateway_pagamento_id,
        )

        return new_payment.execute()

    except SignatureExpired:
        return {"error": "Token expirado."}, 401

    except BadTimeSignature:
        return {"error": "Token inválido."}, 401

    except BadSignature:
        return {"error": "Token inválido."}, 401

    except Exception as exception:
        logging.error(exception)
        return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500


@checkout_controller.get("/listar-todas-doacoes")
@api.validate(
    query=ListarDoacoesQuery,
    resp=Response(
        HTTP_200=ListarDoacoesResponse,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Checkout"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def lista_todas_doacoes():
    """
    Lista todas as doações.
    """
    try:
        repository = CheckoutRepository(db)
        controller = ListaTodasDoacoes(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error


@checkout_controller.put("/include-donation/<int:fk_processamento_pedido_id>")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_404=None, HTTP_500=None),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "editar")
def include_donation(fk_processamento_pedido_id: int):
    """Define se um processamento pedido ou pedido devem ser incluídos ou não na contabilidade de doações"""
    try:

        include_donation = IncludeDonations(fk_processamento_pedido_id)
        response = response_handler(include_donation.execute(), save_logs=True)
        return response

    except Exception as err:
        error_response = errors_handler(err)
        return error_response


@checkout_controller.get("/card-donations-previstas")
@api.validate(
    resp=Response(
        HTTP_200=ReponseCardRecurrencePlanned,
        HTTP_204=None,
        HTTP_404=None,
        HTTP_500=None,
    ),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def card_donations_previstas():
    try:

        card_recurrence_planned = CardRecurrencePlanned(db)
        response = response_handler(
            card_recurrence_planned.execute(), save_logs=True
        )
        return response

    except Exception as er:
        error_response = errors_handler(er, save_logs=True)
        return error_response


@checkout_controller.get("/list-recurrence-donations-made")
@api.validate(
    resp=Response(
        HTTP_200=ResponseDonationsRecurrenceMade,
        HTTP_204=None,
        HTTP_404=None,
        HTTP_500=None,
    ),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def list_donations_recurrence():
    try:
        recurrence_donations_made = RecurrenceDonationsMade()
        response = response_handler(
            recurrence_donations_made.execute(), save_logs=True
        )
        return response
    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        return response_error


@checkout_controller.get("/list-doacoes-nao-efetuadas")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_200=None, HTTP_404=None, HTTP_500=None),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def doacoes_nao_efetuadas():
    try:

        list_recurrence_not_paids = ListingRecurrenceNotPaid()
        response = response_handler(
            list_recurrence_not_paids.execute(), save_logs=True
        )
        return response
    except Exception as err:
        response = errors_handler(err, save_logs=True)
        return response


@checkout_controller.get("/list-doacoes-previstas")
@api.validate(
    resp=Response(
        HTTP_204=None, HTTP_200=ResponsePlanned, HTTP_404=None, HTTP_500=None
    ),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def doacoes_previstas():
    try:
        donations_planned = DonationsPlanned(db)
        response = response_handler(
            donations_planned.execute(), save_logs=True
        )
        return response
    except Exception as e:
        error_response = errors_handler(e, save_logs=True)
        return error_response


@checkout_controller.post("/user-include-donations")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_404=None, HTTP_500=None),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "editar")
def user_include_donations():
    """Adiciona CNPJ E CPF na lista de doações não contabilizadas
    tipo_acao = 1 : adiciona
    tipo_acao = 2 : remove
    """
    try:
        handler_list_exception = AddUserExceptDonations()
        response = response_handler(
            handler_list_exception.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@checkout_controller.get("/list-exception-donations")
@api.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_200=ResponseDonationsExceptions,
        HTTP_404=None,
        HTTP_500=None,
    ),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def list_exception_donations():
    """Retorna lista de usuarios cuajas doações não são contabilizadas"""

    try:
        except_donations = ListingExceptionDonations()
        response = response_handler(except_donations.execute(), save_logs=True)
        return response
    except Exception as e:
        error_response = errors_handler(e, save_logs=True)
        return error_response


@checkout_controller.get("/card-recurrence-donations")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_404=None, HTTP_500=None),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def card_recurrence_donations():
    try:

        card_donations_recurrences = CardRecurrenceDonations()
        response = response_handler(
            card_donations_recurrences.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@checkout_controller.get("/doacoes-desconsideradas")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Pedidos"])
@jwt_required()
@permission_required("doacoes", "acessar")
def list_doacoes_desconsideradas():

    try:
        recurrences_not_contabilizaded = DonationsNotContabilizaded()
        response = response_handler(
            recurrences_not_contabilizaded.execute(), save_logs=True
        )
        return response
    except Exception as err:
        error_response = errors_handler(err, save_logs=True)
        return error_response


@checkout_controller.get("/doacoes-recorrentes-nao-efetivadas")
@api.validate(
    query=ListagemDeRecorreciaEmLapsosRequest,
    resp=Response(
        HTTP_200=None, 
        HTTP_500=None
    ), tags=["Pedidos"])
@jwt_required()
@permission_required("doacoes", "acessar")
def get_doacoes_recorrentes_nao_pagas():
    """Retornar listagem de doações recorrentes não pagas a 4 meses"""
    try:
        repository = CheckoutRepository(db) 
        donations = ListingDoacoesInadimplentes(repository)
        response = response_handler(donations.execute(), save_logs=True)
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error


@checkout_controller.get("/transacoes/<int:fk_pedido_id>")
@api.validate(
    resp=Response(HTTP_200=ResponseListTransaction, HTTP_500=None),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def get_transactions(fk_pedido_id: int):
    try:
        transacao = ListTransactionById(fk_pedido_id)
        response = response_handler(transacao.execute(), save_logs=True)
        return response
    except Exception as e:
        error_response = errors_handler(e, save_logs=True)
        return error_response


@checkout_controller.get("/listar-recorrencias-canceladas")
@api.validate(
    query=ListarRecorrenciasCanceladasQuery,
    resp=Response(
        HTTP_200=ListarRecorrenciasCanceladasResponse,
        HTTP_500=None),
    tags=["Pedidos"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def listar_recorrencias_canceladas():
    """Retorna listagem de doações recorrentes canceladas"""
    try:
        repository = CheckoutRepository(db)
        controller = ListarRecorrenciasCanceladas(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as err:
        error_response = errors_handler(err, save_logs=True)
        return error_response


@checkout_controller.get("/card-recorrencias-canceladas")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Pedidos"])
@jwt_required()
@permission_required("doacoes", "acessar")
def card_recorrencias_canceladas():
    """Retornar quantidade de doações recorrentes canceladas"""
    try:

        query = (
            db.session.query(
                db.func.sum(Pedido.valor_total_pedido),
                db.func.count(Pedido.id),
            )
            .filter(
                Pedido.status_pedido == 2,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == False,
                Pedido.contabilizar_doacao == True,
            )
            .all()
        )

        valor_total_pedidos_cancelados, total_pedidos_cancelados = query[0]

        return {
            "quantidade_canceladas": total_pedidos_cancelados,
            "valor_total_canceladas": round(valor_total_pedidos_cancelados, 2),
        }, 200

    except Exception as err:
        error_response = errors_handler(err, save_logs=True)
        return error_response


@checkout_controller.get("/listar-top-doadores-assiduos")
@api.validate(
    query=GetTopRegularDonorsQueryFilter,
    resp=Response(
        HTTP_200=GetTopRegularDonorsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Benfeitores"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def get_tops_regular_donors():
    """
    Retorna os tops doadores assíduos
    """
    try:
        file_service = file_service_factory()
        repository = CheckoutRepository(db)
        top_donors = GetTopRegularDonors(repository, file_service)
        response = response_handler(top_donors.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@checkout_controller.get("/listar-ranking-doadores")
@api.validate(
    query=GetDonorsRankingQueryFilter,
    resp=Response(
        HTTP_200=GetDonorsRankingResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Benfeitores"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def get_donors_ranking():
    """
    Retorna o ranking de doadores
    """
    try:
        repository = CheckoutRepository(db)
        donors_ranking = GetDonorsRanking(repository)
        response = response_handler(donors_ranking.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@checkout_controller.get("/listar-doadores-assiduos")
@api.validate(
    query=GetRegularDonorsQueryFilter,
    resp=Response(
        HTTP_200=GetRegularDonorsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Benfeitores"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def get_regular_donors():
    """
    Retorna os doadores assíduos
    """
    try:
        repository = CheckoutRepository(db)
        regular_donors = GetRegularDonors(repository)
        response = response_handler(regular_donors.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@checkout_controller.get("/exportar-doacoes")
@api.validate(
    query=ListarDoacoesQuery,
    resp=Response(
        HTTP_200=ExportarDoacoesResponse, 
        HTTP_500=None
        ), 
    tags=["Exporta-Doações"])
@jwt_required()
@permission_required("doacoes", "acessar")
def export_donations():
    """Gerar um relatório csv das doações com base nos filtros."""
    try:
        repository = CheckoutRepository(db)
        controller = ExportarDoacoes(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as err:
        return errors_handler(err, save_logs=True)


@checkout_controller.get("/export-recurrences-made")
@api.validate(
    query=ExportarRecorrenciasAtivasRequest,
    resp=Response(
        HTTP_200=ExportarDoacoesResponse, 
        HTTP_500=None
    ), tags=["Exporta-Doações"]
)
@jwt_required()
@permission_required("doacoes", "acessar")
def export_donations_recurrence():
    """Exporta um relatório de doações recorrentes pagas"""
    try:
        made = ExportDonationsRecurrencesMade(db)
        response = response_handler(made.execute(), save_logs=True)
        return response
    except Exception as err:
        return errors_handler(err, save_logs=True)


@checkout_controller.get("/export-recurrences-planned")
@api.validate(
    query=ExportarRecorrenciasAtivasRequest,
    resp=Response(
        HTTP_200=ExportarDoacoesResponse, 
        HTTP_500=None
    ), tags=["Exporta-Doações"]
)
@jwt_required()
@permission_required("doacoes", "acessar")
def export_donations_recurrence_planned():
    """Exporta um relatório de doações recorrentes previstas"""
    try:
        planned = ExportRecurrencesPlanned(db)
        response = response_handler(planned.execute(), save_logs=True)
        return response
    except Exception as e:
        return errors_handler(e, save_logs=True)


@checkout_controller.get("/export-recurrences-not-paid")
@api.validate(
    query=ExportarRecorrenciasAtivasRequest,
    resp=Response(
        HTTP_200=ExportarDoacoesResponse, 
        HTTP_500=None), 
    tags=["Exporta-Doações"]
)
@jwt_required()
@permission_required("doacoes", "acessar")
def export_donations_recurrence_not_paide():
    """Exporta um relatório de doações recorrentes não pagas"""
    try:
        not_paide = ExportRecurrencesNotPaid(db)
        response = response_handler(not_paide.execute(), save_logs=True)
        return response
    except Exception as err:
        return errors_handler(err, save_logs=True)


@checkout_controller.get("/export-donations-desconsideradas")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_500=None), tags=["Exporta-Doações"]
)
@jwt_required()
@permission_required("doacoes", "acessar")
def doacoes_desconsideradas():
    try:
        obj = ExportDonationsDesconsideradas(db)
        response = response_handler(obj.execute(), save_logs=True)
        return response
    except Exception as err:
        return errors_handler(err, save_logs=True)


@checkout_controller.get("/export-donations-canceladas")
@api.validate(
    query=ListarRecorrenciasCanceladasQuery,
    resp=Response(
        HTTP_200=ExportarDoacoesResponse,
        HTTP_500=None
    ), tags=["Exporta-Doações"]
)
@jwt_required()
@permission_required("doacoes", "acessar")
def doacoes_canceladas():
    try:
        doanations_canceladas = ExportDonationsCanceladas(db)
        response = response_handler(
            doanations_canceladas.execute(), save_logs=True
        )
        return response
    except Exception as err:
        return errors_handler(err, save_logs=True)
        
    
@checkout_controller.get("/exportar-doacoes-recorrentes-em-lapsos")
@api.validate(
    query=ListagemDeRecorreciaEmLapsosRequest,
    resp=Response(
        HTTP_200=ExportarDoacoesResponse, 
        HTTP_500=None
    ), tags=["Exporta-Doações"])
@jwt_required()
@permission_required("doacoes", "acessar")
def get_doacoes_recorrentes_em_lapsos():
    """Exporta listagem de doações recorrentes não pagas a 4 meses"""
    try:
        repository = CheckoutRepository(db) 
        controller = ExportarDoacoesEmLapsos(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error
    

@checkout_controller.post("/enviar-lembrete-email-doacao-nao-paga")
@api.validate(
    json=SendReminderUnpaidDonationRequest,
    resp=Response(HTTP_200=DefaultResponseSchema, HTTP_500=None),
    tags=["Pedido"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def enviar_lembrete_email_doacao_nao_paga():
    try:
        file_service = file_service_factory()

        enviar_lembrete = SendReminderUnpaidDonation(db, file_service)
        response = response_handler(enviar_lembrete.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@checkout_controller.get("/card-lembretes-efetivos")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Pedido"])
@jwt_required()
@permission_required("doacoes", "acessar")
def card_lembretes_efetivos():
    try:
        result = (
            db.session.query(
                db.func.count(ProcessamentoPedido.id).label("qtd_doacoes"),
                db.func.count(db.distinct(Clifor.id)).label("qtd_doadores"),
                db.func.sum(ProcessamentoPedido.valor).label("valor_total"),
            )
            .join(Clifor, Clifor.id == ProcessamentoPedido.fk_clifor_id)
            .filter(
                ProcessamentoPedido.data_lembrete_doacao.isnot(None),
                ProcessamentoPedido.status_processamento == 1,
            )
            .first()
        )

        response = {
            "qtd_doacoes": result.qtd_doacoes or 0,
            "qtd_doadores": result.qtd_doadores or 0,
            "valor_total": round(result.valor_total or 0, 2),
        }

        return jsonify(response), 200

    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {
            "error": "Ocorreu um erro ao retornar os dados do card de lembretes efetivos."
        }, 500
