from flask_jwt_extended import jwt_required
from flask import Blueprint
from spectree import Response
from exceptions.errors_handler import errors_handler
from handlers.generais.create.create_general import CreateGeneral
from handlers.generais.create.registrar_general_wordpress import RegisterGeneralWordPress
from handlers.generais.delete.delete_general import DeleteGeneral

from handlers.generais.get.get_all_generais import GetAllGenerais
from handlers.generais.get.get_all_marechais import ListMarechais
from handlers.generais.get.leads_count import LeadsCount
from handlers.generais.put.update_status_general import UpdateStatusGeneral
from handlers.users.post.register_anonymous_user_full import RegisterAnonymousUserFull
from handlers.users.post.register_deleted_user_full import RegisterDeletedUserFull
from models.schemas.admin.post.register_general import FormGeneralWordPressRequest, RegisterGeneralRequest
from models.schemas.generais.schema_get_all_generais import (
    QuerysGetAllGenerais,
    ResponseGetAllGenerais,
)
from utils.verify_permission import permission_required
from utils.response import (
    DefaultResponseSchema,
    DefaultErrorResponseSchema,
    response_handler,
)
from models.cargo_usuario import (
    UserMarshalResponseListSchema,
    MarshalGeneralQuerySchema,
    UserMarshalQuerySchema,
)
from handlers.generais.promove_general import AlterCargoGeneral
from builder import api, db
from utils.export_generais import ExportGenerais

group_controller = Blueprint(
    "group_controller", __name__, url_prefix="/groups"
)


@group_controller.get("/get-all-general")
@api.validate(
    query=QuerysGetAllGenerais,
    resp=Response(
        HTTP_200=ResponseGetAllGenerais,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Grupos"],
)
@jwt_required()
@permission_required("general", "acessar")
def get_all_generals():
    """Retornar listagem de generais"""
    try:
        get_generais = GetAllGenerais(db)
        response = response_handler(get_generais.execute(), save_logs=True)
        return response
    except Exception as e:
        return errors_handler(e, save_logs=True)


@group_controller.put("/alter-cargo-general/<int:fk_general_id>")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Grupos"],
)
@jwt_required()
@permission_required("general", "editar")
def alter_cargo_general(fk_general_id):
    """Altera o cargo de um general"""
    try:
        alter_cargo = AlterCargoGeneral(fk_general_id, db)
        response = response_handler(alter_cargo.execute(), save_logs=True)
        return response
    except Exception as err:
        return errors_handler(err)


@group_controller.put("/alter-status-general/<int:fk_general_id>")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Grupos"],
)
@jwt_required()
@permission_required("general", "editar")
def alter_status_general(fk_general_id):
    """Altera o status de um general"""
    try:
        alter_status = UpdateStatusGeneral(fk_general_id, db)
        response = response_handler(alter_status.execute(), save_logs=True)
        return response
    except Exception as err:
        return errors_handler(err)


@group_controller.post("/registrar-general")
@api.validate(
    form=RegisterGeneralRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Grupos"],
)
def create_general():
    """Registra um general"""
    try:
        create = CreateGeneral(db)
        response = response_handler(create.execute())
        return response
    except Exception as exception:
        db.session.rollback()
        error_response = errors_handler(exception)
        return error_response


@group_controller.get("/list-marechais")
@api.validate(
    query=UserMarshalQuerySchema,
    resp=Response(
        HTTP_200=UserMarshalResponseListSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Grupos"],
)
@jwt_required()
@permission_required("general", "acessar")
def get_marshal_users():
    """
    Lista nomes de marechais
    """
    try:
        marechais = ListMarechais(db)
        return response_handler(marechais.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)


@group_controller.delete("/delete-general/<int:general_id>")
@api.validate(
    query=MarshalGeneralQuerySchema,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Grupos"],
)
@jwt_required()
@permission_required("general", "deletar")
def delete_generals(general_id):
    """Deleta general"""
    try:
        delete = DeleteGeneral(general_id, db)
        response = response_handler(delete.execute(), save_logs=True)
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@group_controller.get("/export-info-generais")
@api.validate(
    query=MarshalGeneralQuerySchema,
    resp=Response(
        HTTP_200=None,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Grupos"],
)
@jwt_required()
@permission_required("general", "acessar")
def export_info_generais():
    """Exporta generais com base nos filtros"""
    try:

        obj = ExportGenerais(db)
        response = response_handler(obj.execute(), save_logs=True)
        return response
    except Exception as err:
        return errors_handler(err, save_logs=True)


# @group_controller.get("/export-fotos-generais")
# @api.validate(
#     query=MarshalGeneralQuerySchema,
#     resp=Response(
#         HTTP_200=None,
#         HTTP_404=DefaultErrorResponseSchema,
#         HTTP_500=DefaultErrorResponseSchema,
#     ),
#     tags=["Grupos"],
# )
# @jwt_required()
# @permission_required("general", "acessar")
# def export_foto_generais():
#     """Exporta fotos de generais para .zip"""
#     try:
#         download = ExportFotosGenerais(db, file_service_factory)
#         return response_handler(download.execute(), save_logs=True)
#     except Exception as e:
#         return errors_handler(e)


@group_controller.get("/leads-count")
@api.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("usuario", "acessar")
def count_users():
    """Retorna quantidade de usuário por data"""
    try:
        leads_count = LeadsCount(db)
        response = response_handler(leads_count.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@group_controller.post("/registrar-general-wordpress")
@api.validate(
    form=FormGeneralWordPressRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Grupos"],
)
def create_general_word_press():
    """Registra um general via wordpress"""
    try:
        
        caso_usuario_deletado = RegisterDeletedUserFull()
        caso_usuario_anonimo = RegisterAnonymousUserFull()
        
        create = RegisterGeneralWordPress(db, caso_usuario_deletado, caso_usuario_anonimo)
        response = response_handler(create.execute())
        return response
    except Exception as exception:
        db.session.rollback()
        error_response = errors_handler(exception)
        return error_response
