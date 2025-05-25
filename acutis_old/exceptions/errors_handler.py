import logging
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_forbidden import ForbiddenError
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unauthorized import UnauthorizedError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from exceptions.exception_itau import ItauChavePixWebhookException
from utils.logs_access import log_access
from flask_jwt_extended import current_user, get_jwt_identity


def errors_handler(error: Exception, *, save_logs: bool = False):
    errors_types = (
        ItauChavePixWebhookException,
        BadRequestError,
        UnauthorizedError,
        ForbiddenError,
        NotFoundError,
        ConflictError,
        HttpUnprocessableEntity,
    )
    if isinstance(error, errors_types):
        response = {"error": error.error_message}, error.status_code
        print(f"{str(type(error))} - {str(error)}")
        if save_logs and get_jwt_identity() is not None:
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["nome_perfil"],
            )

        return response

    logging.error(f"{str(type(error))} - {str(error)}")
    print(f"{str(type(error))} - {str(error)}")
    return {
        "error": "Erro interno no servidor, tente novamente mais tarde!"
    }, 500
