from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from spectree import Response
from flask import Blueprint

from exceptions.errors_handler import errors_handler
from handlers.auth.post.forgot_password import ForgotPassword
from handlers.auth.post.login import Login
from handlers.auth.post.new_password import NewPassword
from models.schemas.auth.post.forgot_password import ForgotPasswordRequest
from models.schemas.auth.post.login import LoginRequest
from models.schemas.auth.post.new_password import (
    NewPasswordQuery,
    NewPasswordRequest,
)
from utils.response import (
    DefaultErrorResponseSchema,
    DefaultResponseSchema,
    response_handler,
)
from builder import api, db as database
from config import BLACKLIST
from utils.token_email import verify_token

auth_controller = Blueprint("auth_controller", __name__, url_prefix="/auth")


@auth_controller.post("/login")
@api.validate(
    json=LoginRequest,
    resp=Response(
        HTTP_200=None,
        HTTP_400=None,
        HTTP_401=None,
        HTTP_500=None,
    ),
    security={},
    tags=["Autenticação"],
)
def login():
    """
    Autentica o usuário e retorna um token de acesso
    """
    try:
        log_in = Login(database)
        response = response_handler(log_in.execute())
        return response

    except Exception as exception:
        response = errors_handler(exception)
        return response


@auth_controller.post("/refresh")
@api.validate(resp=Response(HTTP_200=None), tags=["Autenticação"])
@jwt_required(refresh=True)
def refresh_token():
    """Gera um novo access token para o usuário"""
    identity = get_jwt_identity()

    return {"access_token": create_access_token(identity=identity)}, 200


@auth_controller.post("/logout")
@api.validate(
    resp=Response(HTTP_200=DefaultResponseSchema), tags=["Autenticação"]
)
@jwt_required(verify_type=False)
def logout():
    """
    Desloga o usuário e revoga o token de acesso
    """
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return {"msg": "Usuário deslogado com sucesso!"}


@auth_controller.post("/forgot-password")
@api.validate(
    json=ForgotPasswordRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_400=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Autenticação"],
)
def post_forgot_password():
    """Envia um email para recuperar a senha da conta"""
    try:
        forgot_password = ForgotPassword()
        response = response_handler(forgot_password.execute())
        return response

    except Exception as err:
        error_response = errors_handler(err)
        return error_response


@auth_controller.post("/new-password")
@api.validate(
    query=NewPasswordQuery,
    json=NewPasswordRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    security={},
    path_parameter_descriptions={
        "token": "Token enviado por email para alterar a senha"
    },
    tags=["Autenticação"],
)
def post_new_password():
    """Altera a senha do usuário deslogado"""
    try:
        new_password = NewPassword(database)
        response = response_handler(new_password.execute())
        return response

    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response

