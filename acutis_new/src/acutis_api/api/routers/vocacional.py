from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.vocacional import (
    AtualizarAndamentoVocacionalUseCase,
    DecodificarTokenVocacionalUseCase,
    DeletarVocacionalUseCase,
    ListarCadastrosVocacionaisUseCase,
    ListarDesistenciasVocacionaisUseCase,
    ListarFichasVocacionaisUseCase,
    ListarPreCadastrosUseCase,
    ListarVocacionaisRecusadosUseCase,
    ReenviarEmailVocacionalUseCase,
    RegistrarCadastroVocacionalUseCase,
    RegistrarDesistenciaVocacionalUseCase,
    RegistrarFichaVocacionalUseCase,
    RegistrarPreCadastroUseCase,
)
from acutis_api.communication.requests.vocacional import (
    AtualizarAndamentoVocacionalRequest,
    ListarCadastrosVocacionaisQuery,
    ListarDesistenciaVocacionaisQuery,
    ListarFichasVocacionaisQuery,
    ListarPreCadastrosQuery,
    ListarVocacionaisRecusadosQuery,
    RegistrarCadastroVocacionalRequest,
    RegistrarFichaVocacionalFormData,
    RegistrarPreCadastroRequest,
    RenviarEmailVocacionalRequest,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.communication.responses.vocacional import (
    DecodificarTokenVocacionalResponse,
    ListarCadastrosVocacionaisResponse,
    ListarDesistenciasVocacionaisResponse,
    ListarFichasVocacionaisResponse,
    ListarPreCadastrosResponse,
    ListarVocacionaisRecusadosResponse,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.vocacional import (
    VocacionalRepository,
)
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.services.sendgrid import SendGridService

vocacional_bp = Blueprint('vocacional_bp', __name__, url_prefix='/vocacional')


@vocacional_bp.post('/registrar-pre-cadastro')
@swagger.validate(
    json=RegistrarPreCadastroRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
def registrar_pre_cadastro():
    """
    Registra um pré cadastro
    """
    try:
        repository = VocacionalRepository(database)
        notification = SendGridService()
        controller = RegistrarPreCadastroUseCase(repository, notification)
        controller.execute()
        return {
            'msg': 'Pré-cadastro realizado com sucesso!'
        }, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@vocacional_bp.get('/listar-pre-cadastros')
@swagger.validate(
    query=ListarPreCadastrosQuery,
    resp=Response(
        HTTP_200=ListarPreCadastrosResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_pre_cadastros():
    """
    Lista os pré cadastros
    """
    try:
        repository = VocacionalRepository(database)
        file_service = file_service_factory()
        controller = ListarPreCadastrosUseCase(repository, file_service)
        filtros = ListarPreCadastrosQuery.model_validate(
            flask_request.args.to_dict()
        )
        response = controller.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@vocacional_bp.put('/atualizar-andamento-vocacional')
@swagger.validate(
    json=AtualizarAndamentoVocacionalRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "editar")
def atualizar_andamento_vocacional():
    """
    Aprova ou reprova o usuário para o próximo passo
    """
    try:
        repository = VocacionalRepository(database)
        request = AtualizarAndamentoVocacionalRequest.model_validate(
            flask_request.json
        )
        controller = AtualizarAndamentoVocacionalUseCase(repository)
        response = controller.execute(request)
        return response, HTTPStatus.OK
    except Exception as e:
        return errors_handler(e)


@vocacional_bp.post('/registrar-desistencia/<uuid:usuario_vocacional_id>')
@swagger.validate(
    json=None,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
def registrar_desistencia(usuario_vocacional_id):
    """
    Usuário desiste do processo vocacional
    """
    try:
        repository = VocacionalRepository(database)
        controller = RegistrarDesistenciaVocacionalUseCase(repository)
        controller.execute(usuario_vocacional_id)
        return {
            'msg': 'Sua desistência foi registrada com sucesso.'
        }, HTTPStatus.OK
    except Exception as e:
        return errors_handler(e)


@vocacional_bp.post('/registrar-cadastro-vocacional')
@swagger.validate(
    json=RegistrarCadastroVocacionalRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
def registrar_cadastro_vocacional():
    """
    Registra o cadastro vocacional
    """
    try:
        repository = VocacionalRepository(database)
        request = RegistrarCadastroVocacionalRequest.model_validate(
            flask_request.json
        )
        controller = RegistrarCadastroVocacionalUseCase(repository)
        controller.execute(request)
        return {
            'msg': 'Cadastro vocacional registrado com sucesso.'
        }, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@vocacional_bp.get('/listar-cadastros-vocacionais')
@swagger.validate(
    query=ListarCadastrosVocacionaisQuery,
    resp=Response(
        HTTP_200=ListarCadastrosVocacionaisResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_cadastros_vocacionais():
    """
    Lista os cadastros vocacionais
    """
    try:
        repository = VocacionalRepository(database)
        file_service = file_service_factory()
        controller = ListarCadastrosVocacionaisUseCase(
            repository, file_service
        )
        filtros = ListarCadastrosVocacionaisQuery.model_validate(
            flask_request.args.to_dict()
        )
        response = controller.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as e:
        return errors_handler(e)


@vocacional_bp.post('/registrar-ficha-vocacional')
@swagger.validate(
    form=RegistrarFichaVocacionalFormData,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
def registrar_ficha_vocacional():
    """
    Registra a ficha vocacional
    """
    try:
        request = RegistrarFichaVocacionalFormData(
            ficha_vocacional=flask_request.form['ficha_vocacional'],
            foto_vocacional=flask_request.files['foto_vocacional'],
        )
        s3_client = file_service_factory()
        repository = VocacionalRepository(database)
        controller = RegistrarFichaVocacionalUseCase(s3_client, repository)
        controller.execute(request)
        return {
            'msg': 'Ficha vocacional preenchida com sucesso.'
        }, HTTPStatus.CREATED
    except Exception as e:
        database.session.rollback()
        return errors_handler(e)


@vocacional_bp.get('/listar-fichas-vocacionais')
@swagger.validate(
    query=ListarFichasVocacionaisQuery,
    resp=Response(
        HTTP_200=ListarFichasVocacionaisResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_fichas_vocacionais():
    """
    Lista as fichas vocacionais
    """
    try:
        repository = VocacionalRepository(database)
        file_service = file_service_factory()
        controller = ListarFichasVocacionaisUseCase(repository, file_service)
        filtros = ListarFichasVocacionaisQuery.model_validate(
            flask_request.args.to_dict()
        )
        response = controller.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as e:
        return errors_handler(e)


@vocacional_bp.get('/listar-desistencias-vocacionais')
@swagger.validate(
    query=ListarDesistenciaVocacionaisQuery,
    resp=Response(
        HTTP_200=ListarDesistenciasVocacionaisResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_desistencias_vocacionais():
    """
    Lista as desistências vocacionais
    """
    try:
        repository = VocacionalRepository(database)
        controller = ListarDesistenciasVocacionaisUseCase(repository)
        filtros = ListarDesistenciaVocacionaisQuery.model_validate(
            flask_request.args.to_dict()
        )
        response = controller.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as e:
        return errors_handler(e)


@vocacional_bp.get('/listar-vocacionais-recusados')
@swagger.validate(
    query=ListarVocacionaisRecusadosQuery,
    resp=Response(
        HTTP_200=ListarVocacionaisRecusadosResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def listar_vocacionais_recusados():
    """
    Lista os vocacionais recusados
    """
    try:
        repository = VocacionalRepository(database)
        controller = ListarVocacionaisRecusadosUseCase(repository)
        filtros = ListarVocacionaisRecusadosQuery.model_validate(
            flask_request.args.to_dict()
        )
        response = controller.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@vocacional_bp.get('/decodificar-token-vocacional/<token>')
@swagger.validate(
    resp=Response(
        HTTP_200=DecodificarTokenVocacionalResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
def decodificar_token_vocacional(token):
    """
    Decodifica o token vocacional
    """
    try:
        repository = VocacionalRepository(database)
        controller = DecodificarTokenVocacionalUseCase(repository)
        response = controller.execute(token)
        return response, HTTPStatus.OK
    except Exception as er:
        return errors_handler(er)


@vocacional_bp.post('/reenviar-email-vocacional')
@swagger.validate(
    json=RenviarEmailVocacionalRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "acessar")
def reenviar_email_vocacional():
    try:
        repository = VocacionalRepository(database)
        controller = ReenviarEmailVocacionalUseCase(repository)
        controller.execute()
        return {'msg': 'Email reenviado com sucesso.'}, HTTPStatus.OK
    except Exception as e:
        return errors_handler(e)


@vocacional_bp.delete('/deletar-vocacional/<uuid:fk_usuario_vocacional_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Vocacional'],
)
@jwt_required()
# @verify_permission.permission_required("vocacional", "deletar")
def deletar_vocacional(fk_usuario_vocacional_id):
    try:
        repository = VocacionalRepository(database)
        controller = DeletarVocacionalUseCase(repository)
        controller.execute(fk_usuario_vocacional_id)
        return {
            'msg': 'Usuário vocacional deletado com sucesso.'
        }, HTTPStatus.OK
    except Exception as e:
        database.session.rollback()
        return errors_handler(e)
