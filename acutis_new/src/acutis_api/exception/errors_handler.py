import logging
from http import HTTPStatus

from authlib.integrations.base_client.errors import OAuthError
from pydantic_core import ValidationError

from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.forbidden import HttpForbiddenError
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unauthorized import HttpUnauthorizedError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)
from acutis_api.shared.errors.maxipago import (
    ErroPagamento,
    ErroRecorrenciaNaoEncontrada,
)


def errors_handler(error: Exception):
    errors_types = (
        HttpBadRequestError,
        HttpConflictError,
        HttpForbiddenError,
        HttpNotFoundError,
        HttpUnauthorizedError,
        HttpUnprocessableEntityError,
        ErroPagamento,
        ErroRecorrenciaNaoEncontrada,
    )

    if isinstance(error, errors_types):
        error_response = [
            {
                'msg': error.message,
            }
        ]
        return error_response, error.status_code

    if isinstance(error, ValidationError):
        return error.errors(), HTTPStatus.UNPROCESSABLE_ENTITY

    if isinstance(error, OAuthError):
        logging.error(f'{type(error)} - {str(error)}')
        error_response = [{'msg': 'Acesso negado pelo Google OAuth.'}]
        return error_response, HTTPStatus.UNAUTHORIZED

    logging.error(f'{type(error)} - {str(error)}')
    error_response = [
        {
            'msg': 'Erro interno no servidor.',
        }
    ]
    return error_response, HTTPStatus.INTERNAL_SERVER_ERROR
