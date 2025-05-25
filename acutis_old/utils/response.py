from flask_jwt_extended import current_user, get_jwt_identity
from pydantic import BaseModel

from utils.logs_access import log_access


class DefaultResponseSchema(BaseModel):
    msg: str


class DefaultErrorResponseSchema(BaseModel):
    error: str


class ErrorWithLogResponseSchema(DefaultErrorResponseSchema):
    type_error: str
    msg_error: str


def response_handler(response: tuple, *, save_logs=False):
    if save_logs and get_jwt_identity() is not None:
        log_access(
            response,
            current_user["id"],
            current_user["nome"],
            current_user["nome_perfil"],
        )
    return response
