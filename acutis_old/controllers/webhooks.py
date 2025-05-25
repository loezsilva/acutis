import logging

from flask import Blueprint, request
from handlers.mensageria.webhook.sandgrid import SandgridWebhook
from handlers.payments.webhook.itau import ItauWebhook
from handlers.payments.webhook.maxipago import MaxiPagoWebhook
from handlers.payments.webhook.mercado_pago import MercadoPagoWebhook


webhooks_controller = Blueprint("webhooks_controller", __name__, url_prefix="/webhook")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("webhook_logs.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@webhooks_controller.post("/maxpago")
def webhook_maxpago():
    """Webhook MaxiPago"""
    wh = MaxiPagoWebhook(logger)

    return wh.execute()


@webhooks_controller.post("/mercado-pago/payment-confirmation")
def webhook_mercado_pago():
    """Webhook MercadoPago"""
    wh = MercadoPagoWebhook(logger)

    return wh.execute()


@webhooks_controller.post("/itau/pix")
def webhook_itau():
    """Webhook Itau"""
    wh = ItauWebhook(logger)

    return wh.execute(request)


@webhooks_controller.post("/sendgrid")
def webhook_sandgrid():
    wh = SandgridWebhook(logger)

    return wh.execute()