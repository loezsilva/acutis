import logging
from http import HTTPStatus

import xmltodict
from flask import Blueprint
from flask import request as flask_request

from acutis_api.application.use_cases.webhooks.itau_pix import (
    WebhookItauPixUseCase,
)
from acutis_api.application.use_cases.webhooks.maxipago import (
    WebhookMaxiPagoUseCase,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.webhooks import WebhooksRepository
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.services.itau import ItauPixService
from acutis_api.infrastructure.services.sendgrid import SendGridService

webhooks_bp = Blueprint('webhooks_bp', __name__, url_prefix='/webhooks')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('webhook_logs.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


# TODO: Criar testes para o webhook # NOSONAR
@webhooks_bp.post('/itau/pix')
@swagger.validate(tags=['Webhooks'])
def webhook_itau():
    """Webhook para registrar pagamentos pix pelo Itau"""
    try:
        request = flask_request.json

        repository = WebhooksRepository(database)
        itau_api = ItauPixService()
        notification = SendGridService()
        file_service = file_service_factory()
        usecase = WebhookItauPixUseCase(
            repository, itau_api, notification, file_service
        )

        usecase.execute(request)
        return {}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        logger.error({
            'error': (
                'Ocorreu um erro ao salvar o pagamento no Itau Webhook.'
            ),
            'errorMsg': f'{str(type(exc))} - {str(exc)}',
            'requisicao': request,
        })
        error_response = errors_handler(exc)
        return error_response


@webhooks_bp.post('/maxipago')
@swagger.validate(tags=['Webhooks'])
def webhook_maxipago():
    """Webhook para registrar pagamentos via cartão de credito recorrente"""
    try:
        xml_data = flask_request.get_data(as_text=True)
        if xml_data.startswith('xml=') or xml_data.startswith('<?xml'):
            xml_data = xml_data[xml_data.find('<Request>') :]

        request = xmltodict.parse(xml_data)

        repository = WebhooksRepository(database)
        notification = SendGridService()
        file_service = file_service_factory()
        usecase = WebhookMaxiPagoUseCase(
            repository,
            notification,
            file_service,
        )

        usecase.execute(request)
        return {}, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        logger.error({
            'error': 'Ocorreu um erro ao salvar o pagamento.',
            'errorMsg': f'{str(type(exc))} - {str(exc)}',
            'requisicao': request,
        })
        error_response = errors_handler(exc)
        return error_response
