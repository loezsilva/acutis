from http import HTTPStatus
from builder import db
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from handlers.users.get.busca_por_documento_ou_contato import BuscaIdUsuarioPorValor
from handlers.users.post.register_anonymous_brazilian_user_with_address import (
    RegisterAnonymousBrazilianUserWithAddress,
)
from handlers.users.post.register_anonymous_user_full import (
    RegisterAnonymousUserFull,
)
from handlers.users.post.register_brazilian_user_with_address import (
    RegisterBrazilianUserWithAddress,
)
from handlers.users.post.register_deleted_brazilian_user_with_address import (
    RegisterDeletedBrazilianUserWithAddress,
)
from handlers.users.post.register_deleted_user_full import (
    RegisterDeletedUserFull,
)
from models.clifor import Clifor
from models.schemas.users.post.register_brazilian_user_with_address import (
    RegisterBrazilianUserWithAddressRequest,
)
from exceptions.error_types.http_forbidden import ForbiddenError
from exceptions.errors_handler import errors_handler
from handlers.users.delete.delete_avatar_image import DeleteAvatarImage
from handlers.users.delete.delete_self_account import DeleteSelfAccount
from handlers.users.get.get_by_id.get_card_user_donations import (
    GetCardUserDonations,
)
from handlers.users.get.get_all.get_all_user_donations import (
    GetAllUserDonations,
)
from handlers.users.get.get_all.get_all_user_donations_history import (
    GetAllUserDonationsHistory,
)
from handlers.users.get.get_by_id.get_cpf_registration_status import (
    GetCpfRegistrationStatus,
)
from handlers.users.get.get_by_id.get_user_by_document_number import (
    GetUserByDocumentNumber,
)
from handlers.users.post.register_anonymous_user import RegisterAnonymousUser
from handlers.users.post.register_lead import RegisterLead
from handlers.users.post.register_presence import RegisterPresence
from handlers.users.post.register_user import RegisterUser
from handlers.users.post.register_deleted_user import (
    RegisterDeletedUser,
)
from handlers.users.post.change_password import ChangePassword
from handlers.users.post.register_user_full import RegisterUserFull
from handlers.users.post.upload_avatar_image import UploadAvatarImage
from handlers.users.post.user_active_account import UserActiveAccount
from handlers.users.put.update_user import UpdateUser
from models.schemas.users.get.get_cpf_registration_status import (
    GetCpfRegistrationStatusQuery,
    GetCpfRegistrationStatusResponse,
)
from models.schemas.users.get.get_user_by_document_number import (
    BuscaUsuarioPorContatoOuDocumentoResponse,
    GetUserByDocumentNumberRequest,
    GetUserByDocumentNumberResponse,
)
from models.schemas.users.get.user_me import (
    UserMeResponse,
)
from models.schemas.users.post.register_lead import RegisterLeadFormData
from models.schemas.users.post.register_presence import RegisterPresenceRequest
from models.schemas.users.post.register_user import RegisterUserRequest
from models.schemas.users.post.change_password import ChangePasswordRequest
from models.schemas.users.post.register_user_full import (
    RegisterUserFullFormData,
)
from models.schemas.users.post.upload_avatar_image import (
    UploadAvatarImageRequest,
)
from models.schemas.users.post.user_active_account import (
    UserActiveAccountResponse,
)
from models.schemas.users.put.update_user import UpdateUserFormData
from services.factories import file_service_factory
from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify
from spectree import Response
from utils.functions import is_valid_email
from utils.regex import format_string
from utils.response import (
    DefaultResponseSchema,
    DefaultErrorResponseSchema,
    response_handler,
)
from builder import api, db, limiter
from utils.validator import cpf_cnpj_validator

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")


@user_controller.post("/register")
@api.validate(
    json=RegisterUserRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_400=None,
        HTTP_404=None,
        HTTP_409=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def register_user():
    """
    Cadastra um novo usuário
    """
    try:
        register_deleted_user = RegisterDeletedUser()
        register_anonymous_user = RegisterAnonymousUser()

        register = RegisterUser(
            db, register_deleted_user, register_anonymous_user
        )
        response = response_handler(register.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.put("/update")
@api.validate(
    form=UpdateUserFormData,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_400=None,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Usuários"],
)
@jwt_required()
def update_user():
    """
    Atualiza os dados do usuário
    """
    try:
        file_service = file_service_factory()

        update = UpdateUser(db, file_service)
        response = response_handler(update.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.post("/active-account/<token>")
@api.validate(
    resp=Response(
        HTTP_200=UserActiveAccountResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    path_parameter_descriptions={
        "token": "Token enviado por email para ativar a conta"
    },
    tags=["Usuários"],
)
def active_account(token: str):
    """
    Verifica o email e ativa a conta do usuário
    """
    try:
        active_user_account = UserActiveAccount(db)
        response = response_handler(active_user_account.execute(token))
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.delete("/delete-self-account")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_500=None),
    tags=["Usuários"],
)
@jwt_required()
def delete_account():
    """
    Deleta a conta do usuário logado
    """
    try:
        file_service = file_service_factory()

        delete_self_account = DeleteSelfAccount(db, file_service)
        response = response_handler(
            delete_self_account.execute(), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@user_controller.post("/change-password")
@api.validate(
    json=ChangePasswordRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_400=None,
        HTTP_409=None,
        HTTP_401=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Usuários"],
)
@jwt_required()
def post_change_password():
    """
    Altera a senha do usuário logado
    """
    try:
        change_password = ChangePassword(db)
        response = response_handler(change_password.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@user_controller.get("/me")
@api.validate(
    resp=Response(
        HTTP_200=UserMeResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Usuários"],
)
@jwt_required()
def me():
    """
    Retorna as informações do usuário logado.
    """
    try:
        return UserMeResponse(**current_user), 200
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.get("/me/permissions")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Usuários"])
@jwt_required()
def me_permissions():
    """
    Retorna as permissões do usuário logado.
    """
    try:
        if current_user["super_perfil"] == False:
            raise ForbiddenError(
                "Você não tem permissão para acessar esta rota."
            )

        return jsonify({"permissoes": current_user["permissoes"]}), 200
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@user_controller.post("/create-lead")
@api.validate(
    form=RegisterLeadFormData,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def post_create_lead():
    """Cria pré cadastro de usuário vindo de ações de campanhas."""
    try:
        file_service = file_service_factory()

        create_lead = RegisterLead(db, file_service)
        response = response_handler(create_lead.execute())
        return response
    except Exception as exception:
        db.session.rollback()
        error_response = errors_handler(exception)
        return error_response


@user_controller.get("/doacoes")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Usuários"])
@jwt_required()
def get_user_donations():
    """Listagem de todas as doações do benfeitor"""
    try:
        file_service = file_service_factory()

        get_doacoes = GetAllUserDonations(db, file_service)
        response = get_doacoes.execute()
        return response

    except Exception as exception:
        response = errors_handler(exception)
        return response


@user_controller.get("/card-doacoes")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Usuários"])
@jwt_required()
def get_card_user_donations():
    """Listagem das informações do card de doações do benfeitor"""
    try:
        get_card_doacoes = GetCardUserDonations(db)
        response = get_card_doacoes.execute()
        return response

    except Exception as exception:
        response = errors_handler(exception)
        return response


@user_controller.get("/historico-doacoes/<int:fk_pedido_id>")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_404=None, HTTP_500=None),
    tags=["Usuários"],
)
@jwt_required()
def get_user_donations_history(fk_pedido_id: int):
    """Listagem do historico de doações do benfeitor"""
    try:
        get_historico_doacoes = GetAllUserDonationsHistory(db)
        response = get_historico_doacoes.execute(fk_pedido_id)
        return response

    except Exception as exception:
        response = errors_handler(exception)
        return response


@user_controller.post("/registrar-presenca")
@api.validate(
    json=RegisterPresenceRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Usuários"],
)
@jwt_required()
@limiter.limit("1 per 2 seconds")
def register_presence():
    """
    Registra a presença do usuário na campanha
    """
    try:
        register_presence = RegisterPresence(db)
        response = response_handler(register_presence.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.post("/salvar-foto-perfil")
@api.validate(
    form=UploadAvatarImageRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Usuários"],
)
@jwt_required()
def upload_avatar_image():
    """Realiza o upload da foto de perfil do usuário"""
    try:
        file_service = file_service_factory()

        upload_avatar_image = UploadAvatarImage(db, file_service)
        response = response_handler(upload_avatar_image.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.delete("/deletar-foto-perfil")
@api.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Usuários"],
)
@jwt_required()
def delete_avatar_image():
    """Deleta a foto de perfil do usuário"""
    try:
        file_service = file_service_factory()

        delete_avatar_image = DeleteAvatarImage(db, file_service)
        response = response_handler(delete_avatar_image.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.get("/buscar-status-registro")
@api.validate(
    query=GetCpfRegistrationStatusQuery,
    resp=Response(
        HTTP_200=GetCpfRegistrationStatusResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def get_cpf_registration_status():
    """Retorna se o cpf informado possui cadastro na base de dados"""
    try:
        get_cpf_status = GetCpfRegistrationStatus(db)
        response = response_handler(get_cpf_status.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.post("/buscar-usuario-por-numero-documento")
@api.validate(
    json=GetUserByDocumentNumberRequest,
    resp=Response(
        HTTP_200=GetUserByDocumentNumberResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def get_user_by_document_number():
    try:
        get_user = GetUserByDocumentNumber(db)
        response = response_handler(get_user.execute())
        return response
    except Exception as exception:
        print(exception)
        error_response = errors_handler(exception)
        return error_response


@user_controller.post("/cadastrar-usuario-completo")
@api.validate(
    form=RegisterUserFullFormData,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def register_user_full_data():
    """
    Cadastra um usuário com todos os dados necessários
    """
    try:
        file_service = file_service_factory()
        user_deleted_handler = RegisterDeletedUserFull()
        anonymous_user_handler = RegisterAnonymousUserFull()

        register_user_full = RegisterUserFull(
            db, file_service, user_deleted_handler, anonymous_user_handler
        )
        response = response_handler(register_user_full.execute())
        return response
    except Exception as exception:
        db.session.rollback()
        error_response = errors_handler(exception)
        return error_response


@user_controller.post("/cadastrar-usuarios")
@api.validate(
    json=RegisterBrazilianUserWithAddressRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def register_brazilian_user_with_address():
    """Cadastra um usuário brasileiro"""
    try:
        deleted_user_handler = RegisterDeletedBrazilianUserWithAddress()
        anonymous_user_handler = RegisterAnonymousBrazilianUserWithAddress()
        register_user = RegisterBrazilianUserWithAddress(
            db, deleted_user_handler, anonymous_user_handler
        )
        response = response_handler(register_user.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@user_controller.get('/verificar-cadastro-documento/<string:cpf_cnpj>')
@api.validate(
    security={},
    tags=['Usuários']
)
def verificar_cadastro_documento(cpf_cnpj: str):
    '''
    Verifica se o CPF do usuário já se encontra cadastrado no sistema
    '''
    try:
        cpf_cnpj = format_string(cpf_cnpj, only_digits=True)
        match len(cpf_cnpj):
            case 11:
                tipo_documento = 'cpf'
            case 14:
                tipo_documento = 'cnpj'
            case _:
                raise BadRequestError('Documento inválido.')
            
        cpf_cnpj = cpf_cnpj_validator(cpf_cnpj, tipo_documento)

        usuario_existente = Clifor.query.filter(
            Clifor.cpf_cnpj == cpf_cnpj, Clifor.fk_usuario_id.isnot(None),
        ).first()

        if usuario_existente:
            raise ConflictError(f'{tipo_documento.upper()} já cadastrado.')
        
        return {}, HTTPStatus.NO_CONTENT
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response
    

@user_controller.get('/verificar-cadastro-email/<string:email>')
@api.validate(
    security={},
    tags=['Usuários']
)
def verificar_cadastro_email(email: str):
    '''
    Verifica se o Email do usuário já se encontra cadastrado no sistema
    '''
    try:
        email = is_valid_email(
            email, check_deliverability=True, check_valid_domain=False
        )

        usuario_existente = Clifor.query.filter(
            Clifor.email == email, Clifor.fk_usuario_id.isnot(None),
        ).first()

        if usuario_existente:
            raise ConflictError('Email já cadastrado.')
        
        return {}, HTTPStatus.NO_CONTENT
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response
    
    
@user_controller.get('/verificar-cadastro-telefone/<string:telefone>')
@api.validate(
    resp=Response(
        HTTP_200=BuscaUsuarioPorContatoOuDocumentoResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Usuários"],
)
def verificar_cadastro_telefone(telefone: str):
    '''
    Verifica se o telefone do usuário já se encontra cadastrado no sistema
    '''
    try:
        telefone_formatado = format_string(
            telefone.strip(), only_digits=True
        )

        telefone_existente = Clifor.query.filter(
            Clifor.telefone1 == telefone_formatado, Clifor.fk_usuario_id.isnot(None),
        ).first()
        
        if telefone_existente:
            raise ConflictError('Telefone já cadastrado.')
        
        return {}, HTTPStatus.NO_CONTENT
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response
    
# @user_controller.get('/busca-id-de-usuario/<valor_busca>')
# @api.validate(
#     resp=Response(
#         HTTP_200=BuscaUsuarioPorContatoOuDocumentoResponse,
#         HTTP_500=DefaultErrorResponseSchema,
#     ),
#     security={},
#     tags=["Usuários"],
# )
# def busca_id_usuario_por_dado(valor_busca):
#     try:
#         usecase = BuscaIdUsuarioPorValor(db)
#         response = usecase.execute(valor_busca)
#         return response_handler(response)
#     except Exception as exc:
#         return errors_handler(exc)