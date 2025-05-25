from flask import Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response
from exceptions.errors_handler import errors_handler
from handlers.vocacional.delete.deletetar_vocacional import DeletarVocacional
from handlers.vocacional.get.listar_cadastros_vocacionais import (
    ListarCadastrosVocacional,
)
from handlers.vocacional.get.listar_pre_cadastros import ListarPreCadastros
from handlers.vocacional.post.reenviar_email_vocacional import ReenviarEmailVocacional
from handlers.vocacional.get.listar_desistencias_vocacionais import (
    ListarDesistenciasVocacionais,
)
from handlers.vocacional.get.listar_fichas_vocacionais import ListarFichasVocacionais
from handlers.vocacional.get.decodificar_token_vocacional import (
    DecodificarTokenVocacional,
)
from handlers.vocacional.get.listar_vocacionais_recusados import (
    ListarVocacionaisRecusados,
)
from handlers.vocacional.post.registrar_cadastro_vocacional import (
    RegistrarCadastroVocacional,
)
from handlers.vocacional.post.registrar_ficha_vocacional import RegistrarFichaVocacional
from handlers.vocacional.post.registrar_pre_cadastro import (
    RegistrarPreCadastro,
)
from handlers.vocacional.post.registrar_desistencia_vocacional import (
    RegistrarDesistenciaVocacional,
)
from handlers.vocacional.put.atualizar_andamento_vocacional import (
    AtualizarAndamentoVocacional,
)
from models.schemas.vocacional.get.decodificar_token_vocacional_schema import (
    DecodificarTokenVocacionalResponse,
)
from models.schemas.vocacional.get.listar_fichas_vocacionais_schema import (
    ListarFichasVocacionaisResponse,
    ListarFichasVocacionaisQuery,
)
from models.schemas.vocacional.get.listar_cadastros_vocacionais_schema import (
    ListarCadastrosVocacionaisResponse,
    ListarCadastrosVocacionaisQuery,
)
from models.schemas.vocacional.get.listar_desistencias_vocacionais_schema import (
    DesistenciaVocacionaisQuery,
    ListarDesistenciasVocacionaisResponse,
)
from models.schemas.vocacional.get.listar_pre_cadastros_schema import (
    ListarPreVocacionaisResponse,
    ListarPreCadastrosQuery,
)
from models.schemas.vocacional.get.listar_vocacionais_recusados_schema import (
    VocacionaisRecusadosQuery,
    VocacionaisRecusadosResponse,
)
from models.schemas.vocacional.post.registrar_cadastro_vocacional_request import (
    RegistrarCadastroVocacionalRequest,
)
from models.schemas.vocacional.post.registrar_ficha_vocacional_request import (
    RegistrarFichaVocacionalFormData,
)
from models.schemas.vocacional.post.reenviar_email_vocacioanal_request import (
    RenviarEmailVocacionalRequest,
)
from models.schemas.vocacional.put.atualizar_andamento_vocacional_request import (
    AtualizarAndamentoVocacionalRequest,
)
from models.schemas.vocacional.post.registrar_pre_cadastro_vocacional_request import (
    RegistrarPreCadastroRequest,
)
from repositories.vocacional_repository import VocacionalRepository
from services.factories import file_service_factory
from utils import verify_permission
from utils.response import (
    DefaultErrorResponseSchema,
    DefaultResponseSchema,
    response_handler,
)
from builder import api, db

vocacional_controller = Blueprint(
    "vocacional_controller", __name__, url_prefix="/vocacional"
)


@vocacional_controller.post("/registrar-pre-cadastro")
@api.validate(
    json=RegistrarPreCadastroRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
def registrar_pre_cadastro():
    try:
        repository = VocacionalRepository(db)
        controller = RegistrarPreCadastro(repository)
        response = controller.execute()
        return response_handler(response)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.get("/listar-pre-cadastros")
@api.validate(
    query=ListarPreCadastrosQuery,
    resp=Response(
        HTTP_200=ListarPreVocacionaisResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_pre_cadastros():
    try:
        repository = VocacionalRepository(db)
        controller = ListarPreCadastros(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.put("/atualizar-andamento-vocacional")
@api.validate(
    json=AtualizarAndamentoVocacionalRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "editar")
def atualizar_andamento_vocacional():
    try:
        repository = VocacionalRepository(db)
        controller = AtualizarAndamentoVocacional(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.post("/registrar-desistencia/<int:usuario_vocacional_id>")
@api.validate(
    json=None,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
def registrar_desistencia(usuario_vocacional_id):
    try:
        repository = VocacionalRepository(db)
        controller = RegistrarDesistenciaVocacional(repository)
        response = controller.execute(usuario_vocacional_id)
        return response_handler(response)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.post("/registrar-cadastro-vocacional")
@api.validate(
    json=RegistrarCadastroVocacionalRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
def registrar_cadastro_vocacional():
    try:
        repository = VocacionalRepository(db)
        controller = RegistrarCadastroVocacional(repository)
        response = controller.execute()
        return response_handler(response)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.get("/listar-cadastros-vocacionais")
@api.validate(
    query=ListarCadastrosVocacionaisQuery,
    resp=Response(
        HTTP_200=ListarCadastrosVocacionaisResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_cadastros_vocacionais():
    try:
        repository = VocacionalRepository(db)
        controller = ListarCadastrosVocacional(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.post("/registrar-ficha-vocacional")
@api.validate(
    form=RegistrarFichaVocacionalFormData,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
def registrar_ficha_vocacional():
    try:
        s3_client = file_service_factory()
        repository = VocacionalRepository(db)
        controller = RegistrarFichaVocacional(s3_client, repository)
        response = controller.execute()
        return response_handler(response)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.get("/listar-fichas-vocacionais")
@api.validate(
    query=ListarFichasVocacionaisQuery,
    resp=Response(
        HTTP_200=ListarFichasVocacionaisResponse,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_fichas_vocacionais():
    try:
        repository = VocacionalRepository(db)
        controller = ListarFichasVocacionais(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.get("/listar-desistencias-vocacionais")
@api.validate(
    query=DesistenciaVocacionaisQuery,
    resp=Response(
        HTTP_200=ListarDesistenciasVocacionaisResponse,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_desistencias_vocacionais():
    try:
        repository = VocacionalRepository(db)
        controller = ListarDesistenciasVocacionais(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.get("/listar-vocacionais-recusados")
@api.validate(
    query=VocacionaisRecusadosQuery,
    resp=Response(
        HTTP_200=VocacionaisRecusadosResponse,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_vocacionais_recusados():
    try:
        repository = VocacionalRepository(db)
        controller = ListarVocacionaisRecusados(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.get("/decodificar-token-vocacional/<token>")
@api.validate(
    resp=Response(
        HTTP_200=DecodificarTokenVocacionalResponse,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
def decodificar_token_vocacional(token):
    try:
        repository = VocacionalRepository(db)
        controller = DecodificarTokenVocacional(repository)
        response = controller.execute(token)
        return response_handler(response)
    except Exception as er:
        return errors_handler(er)


@vocacional_controller.post("/reenviar-email-vocacional")
@api.validate(
    json=RenviarEmailVocacionalRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def reenviar_email_vocacional():
    try:
        repository = VocacionalRepository(db)
        controller = ReenviarEmailVocacional(repository)
        response = controller.execute()
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)


@vocacional_controller.delete("/deletar-vocacional/<int:fk_usuario_vocacional_id>")
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Vocacional"],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "deletar")
def deletar_vocacional(fk_usuario_vocacional_id):
    try:
        repository = VocacionalRepository(db)
        controller = DeletarVocacional(repository)
        response = controller.execute(fk_usuario_vocacional_id)
        return response_handler(response, save_logs=True)
    except Exception as e:
        return errors_handler(e)
