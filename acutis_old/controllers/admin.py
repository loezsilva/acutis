from flask import Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response

from exceptions.errors_handler import errors_handler
from builder import api
from builder import db as database
from builder import limiter
from handlers.admin.delete.delete_profile import DeleteProfile
from handlers.admin.delete.delete_user_by_id import DeleteUserById
from handlers.admin.get.get_all.download_leads_photos_batch import (
    DownloadLeadsPhotosBatch,
)
from handlers.admin.get.get_all.export_users_data import ExportUsersData
from handlers.admin.get.get_all.get_all_actions import GetAllActions
from handlers.admin.get.get_all.get_all_actions_names import GetAllActionsNames
from handlers.admin.get.get_all.get_all_birthdays import GetAllBirthdays
from handlers.admin.get.get_all.get_all_leads import GetAllLeads
from handlers.admin.get.get_all.get_all_profiles import GetAllProfiles
from handlers.admin.get.get_all.get_all_users import GetAllUsers
from handlers.admin.get.get_all.get_all_users_permissions import (
    GetAllUsersPermissions,
)
from handlers.admin.get.get_all.get_all_users_presences import (
    GetAllUsersPresences,
)
from handlers.admin.get.get_all.get_card_total_leads import GetCardTotalLeads
from handlers.admin.get.get_all.get_regular_users_quantity import (
    GetRegularUsersQuantity,
)
from handlers.admin.get.get_all.get_winning_leads import GetWinningLeads
from handlers.admin.get.get_by_id.get_action_details_by_id import (
    GetActionDetailsById,
)
from handlers.admin.get.get_by_id.get_address_by_user_id import (
    GetAddressByUserId,
)
from handlers.admin.get.get_by_id.get_profile_by_id import GetProfileById
from handlers.admin.get.get_by_id.get_random_lead_by_action_id import (
    GetRandomLeadByActionId,
)
from handlers.admin.get.get_by_id.get_total_leads_by_action_id import (
    GetTotalLeadsByActionId,
)
from handlers.admin.get.get_by_id.get_user_by_id import GetUserById
from handlers.admin.get.get_by_id.get_user_presence_by_id import (
    GetUserPresenceById,
)
from handlers.admin.patch.update_action_status import UpdateActionStatus
from handlers.admin.post.confirm_selected_lead import ConfirmSelectedLead
from handlers.admin.post.download_leads_photos import DownloadLeadsPhotos
from handlers.admin.post.register_action import RegisterAction
from handlers.admin.post.register_profile import RegisterProfile
from handlers.admin.post.register_user_permission import RegisterUserPermission
from handlers.admin.post.resend_active_account_email import (
    ResendActiveAccountEmail,
)
from handlers.admin.put.update_action import UpdateAction
from handlers.admin.put.update_address_by_user_id import UpdateAddressByUserId
from handlers.admin.put.update_profile_permissions import (
    UpdateProfilePermissions,
)
from handlers.admin.put.update_user_by_id import UpdateUserById
from handlers.admin.put.update_user_permission import UpdateUserPermission
from models.schemas.admin.get.get_all.get_all_actions import (
    GetAllActionsFilters,
    GetAllActionsResponse,
)
from models.schemas.admin.get.get_all.get_all_actions_names import (
    GetAllActionsNamesResponse,
)
from models.schemas.admin.get.get_all.get_all_birthdays import (
    GetAllBirthdaysResponse,
)
from models.schemas.admin.get.get_all.get_all_leads import (
    GetAllLeadsQuery,
    GetAllLeadsResponse,
)
from models.schemas.admin.get.get_all.get_all_profiles import (
    GetAllProfilesResponse,
)
from models.schemas.admin.get.get_all.get_all_users import (
    GetAllUsersQuery,
    GetAllUsersResponse,
)
from models.schemas.admin.get.get_all.get_all_users_permissions import (
    GetAllUsersPermissionsQuery,
    GetAllUsersPermissionsResponse,
)
from models.schemas.admin.get.get_all.get_all_users_presences import (
    GetAllUsersPresencesFilters,
    GetAllUsersPresencesResponse,
)
from models.schemas.admin.get.get_all.get_card_total_leads import (
    GetCardTotalLeadsResponse,
)
from models.schemas.admin.get.get_all.get_winning_leads import (
    GetWinningLeadsFilters,
    GetWinningLeadsResponse,
)
from models.schemas.admin.get.get_by_id.get_action_details_by_id import (
    GetActionDetailsByIdResponse,
)
from models.schemas.admin.get.get_by_id.get_address_user_by_id import (
    GetAddressByUserIdResponse,
)
from models.schemas.admin.get.get_by_id.get_profile_by_id import (
    GetProfileByIdResponse,
)
from models.schemas.admin.get.get_by_id.get_random_lead_by_action_id import (
    GetRandomLeadByActionIdResponse,
)
from models.schemas.admin.get.get_by_id.get_total_leads_by_action_id import (
    GetTotalLeadsByActionIdResponse,
)
from models.schemas.admin.get.get_by_id.get_user_by_id import (
    GetUserByIdResponse,
)
from models.schemas.admin.get.get_by_id.get_user_presence_by_id import (
    GetUserPresenceByIdResponse,
)
from models.schemas.admin.post.confirm_selected_lead import (
    ConfirmSelectedLeadQuery,
    ConfirmSelectedLeadRequest,
)
from models.schemas.admin.post.download_leads_photos import (
    DownloadLeadsPhotosRequest,
)
from models.schemas.admin.post.register_action import RegisterActionFormData
from models.schemas.admin.post.register_profile import RegisterProfileRequest
from models.schemas.admin.post.register_user_permission import (
    RegisterUserPermissionRequest,
)
from models.schemas.admin.put.update_action import UpdateActionFormData
from models.schemas.admin.put.update_address_by_user_id import (
    UpdateAddressByUserIdRequest,
)
from models.schemas.admin.put.update_profile_permissions import (
    UpdateProfilePermissionsRequest,
)
from models.schemas.admin.put.update_user_by_id import UpdateUserByIdRequest
from models.schemas.admin.put.update_user_permission import (
    UpdateUserPermissionRequest,
)
from repositories.admin_repository import AdminRepository
from services.factories import file_service_factory
from utils.export_excel import export_excel
from utils.response import (
    DefaultErrorResponseSchema,
    DefaultResponseSchema,
    response_handler,
)
from utils.verify_permission import permission_required

admin_controller = Blueprint(
    "admin_controller", __name__, url_prefix="/administradores"
)


@admin_controller.get("/listar-usuarios")
@api.validate(
    query=GetAllUsersQuery,
    resp=Response(
        HTTP_200=GetAllUsersResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_all_users():
    """Lista todos os usuários do sistema"""
    try:
        get_all = GetAllUsers(database)
        response = response_handler(get_all.execute(), save_logs=True)
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/buscar-usuario/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetUserByIdResponse,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_user_by_id(fk_usuario_id: int):
    """Busca os dados de um usuário pelo ID"""
    try:
        file_service = file_service_factory()

        get_by_id = GetUserById(database, file_service)
        response = response_handler(
            get_by_id.execute(fk_usuario_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.put("/editar-usuario/<int:fk_usuario_id>")
@api.validate(
    json=UpdateUserByIdRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "editar")
def update_user_by_id(fk_usuario_id: int):
    """Atualiza os dados de um usuário pelo ID"""
    try:
        update_user = UpdateUserById(database)
        response = response_handler(
            update_user.execute(fk_usuario_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.delete("/deletar-usuario/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "deletar")
def delete_user_by_id(fk_usuario_id: int):
    """Deleta um usuário pelo ID"""
    try:
        file_service = file_service_factory()

        delete_user = DeleteUserById(database, file_service)
        response = response_handler(
            delete_user.execute(fk_usuario_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.post("/reenviar-email-ativacao-conta/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "editar")
def post_resend_active_account_email(fk_usuario_id: int):
    """Reenvia o email de ativação de conta para o usuário pelo ID"""
    try:
        resend_active_account_email = ResendActiveAccountEmail()
        response = response_handler(
            resend_active_account_email.execute(fk_usuario_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/buscar-endereco-usuario/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetAddressByUserIdResponse,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("endereco", "acessar")
def get_address_by_user_id(fk_usuario_id: int):
    """Busca o endereço de um usuário pelo ID"""
    try:
        get_address = GetAddressByUserId(database)
        response = response_handler(
            get_address.execute(fk_usuario_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.put("/editar-endereco-usuario/<int:fk_usuario_id>")
@api.validate(
    json=UpdateAddressByUserIdRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("endereco", "editar")
def update_address_by_user_id(fk_usuario_id: int):
    """Atualiza o endereço de um usuário pelo ID"""
    try:
        update_address = UpdateAddressByUserId(database)
        response = response_handler(
            update_address.execute(fk_usuario_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-aniversariantes")
@api.validate(
    resp=Response(
        HTTP_200=GetAllBirthdaysResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_birthdays():
    """Lista todos os aniversariantes"""
    try:
        file_service = file_service_factory()

        get_birthdays = GetAllBirthdays(database, file_service)
        response = response_handler(get_birthdays.execute(), save_logs=True)
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.post("/cadastrar-usuario-perfil")
@api.validate(
    json=RegisterUserPermissionRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_422=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("perfil", "criar")
def register_user_permission():
    """Cadastra uma permissão de usuário"""
    try:
        register_user_permission = RegisterUserPermission(database)
        response = response_handler(
            register_user_permission.execute(), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.put("/editar-usuario-perfil/<int:fk_usuario_id>")
@api.validate(
    json=UpdateUserPermissionRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_422=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
    path_parameter_descriptions={
        "fk_usuario_id": "ID do usuário a ser atualizado"
    },
)
@jwt_required()
@permission_required("perfil", "editar")
def update_user_permission(fk_usuario_id: int):
    """Atualiza o perfil de um usuário pelo ID"""
    try:
        update_user_permission = UpdateUserPermission(database)
        response = response_handler(
            update_user_permission.execute(fk_usuario_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-usuarios-perfil")
@api.validate(
    query=GetAllUsersPermissionsQuery,
    resp=Response(
        HTTP_200=GetAllUsersPermissionsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("perfil", "acessar")
def get_all_users_permissions():
    """Lista todas as permissões de usuários"""
    try:
        users_permissions = GetAllUsersPermissions(database)
        response = response_handler(
            users_permissions.execute(), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.post("/cadastrar-perfil")
@api.validate(
    json=RegisterProfileRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("perfil", "criar")
def register_profile():
    """Cadastra um perfil"""
    try:
        register_profile = RegisterProfile(database)
        response = response_handler(register_profile.execute(), save_logs=True)
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.put("/editar-permissoes-perfil/<int:fk_perfil_id>")
@api.validate(
    json=UpdateProfilePermissionsRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
    path_parameter_descriptions={
        "fk_perfil_id": "ID do perfil a ser atualizado"
    },
)
@jwt_required()
@permission_required("perfil", "editar")
def update_profile(fk_perfil_id: int):
    """Atualiza as permissões de um perfil pelo ID"""
    try:
        update_profile = UpdateProfilePermissions(database)
        response = response_handler(
            update_profile.execute(fk_perfil_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.delete("/deletar-perfil/<int:fk_perfil_id>")
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_409=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("perfil", "deletar")
def delete_profile(fk_perfil_id: int):
    """Deleta um perfil pelo ID"""
    try:
        delete_profile = DeleteProfile(database)
        response = response_handler(
            delete_profile.execute(fk_perfil_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/buscar-perfil/<int:fk_perfil_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetProfileByIdResponse,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("perfil", "acessar")
def get_profile_by_id(fk_perfil_id: int):
    """Busca um perfil pelo ID"""
    try:
        get_profile = GetProfileById(database)
        response = response_handler(
            get_profile.execute(fk_perfil_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-perfis")
@api.validate(
    resp=Response(
        HTTP_200=GetAllProfilesResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("perfil", "acessar")
def get_all_profiles():
    """Lista todos os perfis"""
    try:
        get_all_profiles = GetAllProfiles(database)
        response = response_handler(get_all_profiles.execute(), save_logs=True)
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.post("/cadastrar-acao")
@api.validate(
    form=RegisterActionFormData,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_409=None,
        HTTP_500=DefaultResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "criar")
def register_action():
    """Cadastra uma ação para cadastro de leads"""
    try:
        file_service = file_service_factory()
        register_action = RegisterAction(database, file_service)
        response = response_handler(register_action.execute(), save_logs=True)
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.put("/editar-acao/<int:fk_acao_id>")
@api.validate(
    form=UpdateActionFormData,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
)
@jwt_required()
@permission_required("campanha", "editar")
def update_action(fk_acao_id: int):
    """Atualiza uma ação para cadastro de leads pelo ID"""
    try:
        file_service = file_service_factory()

        update_action = UpdateAction(database, file_service)
        response = response_handler(
            update_action.execute(fk_acao_id), save_logs=True
        )
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.patch("/editar-status-acao/<int:fk_acao_id>")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_404=None, HTTP_500=None),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "editar")
def update_action_status(fk_acao_id: int):
    """Atualiza o status de uma ação pelo ID"""
    try:
        update_action_status = UpdateActionStatus(database)
        response = response_handler(
            update_action_status.execute(fk_acao_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/buscar-detalhes-acao/<int:fk_acao_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetActionDetailsByIdResponse,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    )
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_action_details(fk_acao_id: int):
    """Busca os detalhes de uma ação pelo ID"""
    try:
        file_service = file_service_factory()
        get_action_details = GetActionDetailsById(database, file_service)
        response = response_handler(
            get_action_details.execute(fk_acao_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-acoes")
@api.validate(
    query=GetAllActionsFilters,
    resp=Response(
        HTTP_200=GetAllActionsResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_all_actions():
    """Lista todas as ações"""
    try:
        get_all_actions = GetAllActions(database)
        response = response_handler(get_all_actions.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-nomes-acoes")
@api.validate(
    resp=Response(
        HTTP_200=GetAllActionsNamesResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_all_actions_names():
    """Lista todos os nomes de ações"""
    try:
        get_all_actions_names = GetAllActionsNames(database)
        response = response_handler(get_all_actions_names.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@admin_controller.get("/listar-leads")
@api.validate(
    query=GetAllLeadsQuery,
    resp=Response(
        HTTP_200=GetAllLeadsResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_all_leads():
    """Lista todos os leads"""
    try:
        file_service = file_service_factory()

        all_leads = GetAllLeads(database, file_service)
        response = response_handler(all_leads.execute(), save_logs=True)
        return response

    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.post("/baixar-fotos-leads")
@api.validate(
    json=DownloadLeadsPhotosRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def download_leads_photos():
    """Registra o download das fotos dos leads"""
    try:
        download_leads_photos = DownloadLeadsPhotos(database)
        response = response_handler(
            download_leads_photos.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/card-total-leads")
@api.validate(
    resp=Response(
        HTTP_200=GetCardTotalLeadsResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_card_total_leads():
    """Alimenta o card de total de leads"""
    try:
        get_card_total_leads = GetCardTotalLeads(database)
        response = response_handler(get_card_total_leads.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@admin_controller.get("/sortear-lead-por-acao/<int:fk_acao_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetRandomLeadByActionIdResponse,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_random_lead_by_action_id(fk_acao_id: int):
    """Sorteia um lead aleatório por ação"""
    try:
        get_random_lead_by_action_id = GetRandomLeadByActionId(database)
        response = response_handler(
            get_random_lead_by_action_id.execute(fk_acao_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.post("/confirmar-lead-sorteado")
@api.validate(
    query=ConfirmSelectedLeadQuery,
    json=ConfirmSelectedLeadRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_400=None,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@limiter.limit("1 per 1 seconds")
@permission_required("campanha", "acessar")
def confirm_selected_lead():
    """Confirma a seleção de um lead sorteado"""
    try:
        confirm_selected_lead = ConfirmSelectedLead(database)
        response = response_handler(
            confirm_selected_lead.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-leads-sorteados")
@api.validate(
    query=GetWinningLeadsFilters,
    resp=Response(
        HTTP_200=GetWinningLeadsResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_winning_leads():
    """Lista os leads sorteados"""
    try:
        get_winning_leads = GetWinningLeads(database)
        response = response_handler(
            get_winning_leads.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/total-leads-por-acao/<int:fk_acao_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetTotalLeadsByActionIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_total_leads_by_action_id(fk_acao_id: int):
    """Lista o total de leads por ação"""
    try:
        get_total_leads_by_action_id = GetTotalLeadsByActionId(database)
        response = response_handler(
            get_total_leads_by_action_id.execute(fk_acao_id)
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@admin_controller.get("/baixar-fotos-leads-lote")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_500=None), tags=["Administradores"]
)
@jwt_required()
@permission_required("usuario", "acessar")
def download_leads_photos_batch():
    """Registra o download das fotos dos leads"""
    try:
        file_service = file_service_factory()

        download_leads_photos_batch = DownloadLeadsPhotosBatch(
            database, file_service
        )
        response = download_leads_photos_batch.execute()
        log_tuple = (str(response[0]), response[1])
        response_handler(log_tuple, save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/listar-presencas-usuarios")
@api.validate(
    query=GetAllUsersPresencesFilters,
    resp=Response(
        HTTP_200=GetAllUsersPresencesResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_all_users_presences():
    """Lista todas as presenças dos usuários"""
    try:
        file_service = file_service_factory()

        get_all_users_presences = GetAllUsersPresences(database, file_service)
        response = response_handler(
            get_all_users_presences.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/buscar-presenca/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetUserPresenceByIdResponse,
        HTTP_404=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Administradores"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_user_presence_by_id(fk_usuario_id: int):
    """Busca a presença de um usuário pelo ID"""
    try:
        get_user_presence_by_id = GetUserPresenceById(database)
        response = response_handler(
            get_user_presence_by_id.execute(fk_usuario_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/exportar-dados-usuarios")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_500=None), tags=["Administradores"]
)
@jwt_required()
@permission_required("usuario", "acessar")
def export_users_data():
    """Exporta os dados dos usuários para um arquivo CSV"""
    try:
        admin_repository = AdminRepository(database)
        export_users_data = ExportUsersData(admin_repository, export_excel)
        response = response_handler(
            export_users_data.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@admin_controller.get("/quantidade-usuarios-regulares")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_500=None), tags=["Administradores"]
)
@jwt_required()
@permission_required("usuario", "acessar")
def get_regular_users_quantity():
    """Busca a quantidade de usuários regulares"""
    try:
        admin_repository = AdminRepository(database)
        regular_users_quantity = GetRegularUsersQuantity(admin_repository)
        response = response_handler(regular_users_quantity.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response
