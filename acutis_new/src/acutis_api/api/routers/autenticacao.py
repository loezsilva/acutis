from http import HTTPStatus

from flask import Blueprint, make_response, request, session
from flask import request as flask_request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from spectree import Response

from acutis_api.application.use_cases.autenticacao.buscar import (
    UsuarioLogadoUseCase,
)
from acutis_api.application.use_cases.autenticacao.login import (
    AlterarSenhaUseCase,
    BuscaCadastroPorEmail,
    GoogleCallbackUseCase,
    LoginGoogleUseCase,
    LoginUseCase,
    NovaSenhaUseCase,
    RecuperarSenhaUseCase,
    VerificarTokenAtivacaoContaUseCase,
)
from acutis_api.application.use_cases.autenticacao.login.ativar_conta import (
    AtivarContaUseCase,
)
from acutis_api.communication.requests.autenticacao import (
    AlterarSenhaRequest,
    AtivarContaRequest,
    LoginRequest,
    NovaSenhaQuery,
    NovaSenhaRequest,
    RecuperarSenhaRequest,
    UsarHttpOnlyQuery,
    VerificarTokenRequest,
)
from acutis_api.communication.responses.autenticacao import (
    UsuarioLogadoResponse,
    VerificarTokenResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import (
    BLACKLIST,
    database,
    oauth,
    swagger,
)
from acutis_api.infrastructure.repositories.autenticacao import (
    AutenticacaoRepository,
)
from acutis_api.infrastructure.repositories.membros import MembrosRepository
from acutis_api.infrastructure.services.sendgrid import SendGridService

autenticacao_bp = Blueprint(
    'autenticacao_bp', __name__, url_prefix='/autenticacao'
)


oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': ['openid', 'email', 'profile']},
)


@autenticacao_bp.post('/login')
@swagger.validate(
    query=UsarHttpOnlyQuery,
    json=LoginRequest,
    tags=['Autenticação'],
)
def login():
    """
    Realiza o login do membro
    """
    try:
        request = LoginRequest.model_validate(flask_request.json)
        query = UsarHttpOnlyQuery.model_validate(flask_request.args.to_dict())

        repository = AutenticacaoRepository(database)
        notification = SendGridService()

        usecase = LoginUseCase(repository, notification)
        response = usecase.execute(request, query)

        return response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@autenticacao_bp.post('/refresh')
@swagger.validate(tags=['Autenticação'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Renova o token de autenticação do membro
    """
    identity = get_jwt_identity()
    novo_access_token = create_access_token(identity=identity)

    if 'Authorization' in request.headers:
        response = {'access_token': novo_access_token}
    else:
        response = make_response()
        set_access_cookies(response, novo_access_token)

    return response, HTTPStatus.OK


@autenticacao_bp.delete('/revogar-tokens')
@swagger.validate(tags=['Autenticação'])
@jwt_required(verify_type=False)
def logout():
    """
    Desloga o membro e revoga o tokens de acesso
    """
    response = make_response()

    if 'Authorization' in request.headers:
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
    else:
        unset_jwt_cookies(response)

    return response, HTTPStatus.NO_CONTENT


@autenticacao_bp.get('/google/authorize')
@swagger.validate(tags=['Autenticação'])
def login_google():
    """
    Redireciona o membro para realizar o login pelo Google Auth
    """
    try:
        session['original_url'] = request.referrer
        session['google_auth'] = True

        google = oauth.create_client('google')

        usecase = LoginGoogleUseCase(google)
        return usecase.execute()

    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


# TODO: Remover rota de teste # NOSONAR
@autenticacao_bp.get('/teste-autenticacao')
@jwt_required()
def teste_autenticacao():
    return {'msg': 'Usuario autenticado com sucesso!'}


@autenticacao_bp.get('/google/callback')
@swagger.validate(tags=['Autenticação'])
def google_callback():
    """
    Retorna os dados do lead pelo Google Auth
    """
    try:
        google = oauth.create_client('google')
        repository = MembrosRepository(database)
        notification = SendGridService()

        usecase = GoogleCallbackUseCase(google, repository, notification)
        response = usecase.execute()

        return response, HTTPStatus.FOUND
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@autenticacao_bp.post('/verificar-token-ativacao-de-conta')
@swagger.validate(
    json=VerificarTokenRequest,
    resp=Response(
        HTTP_200=VerificarTokenResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Autenticação'],
)
def verificar_token():
    """
    Verifica o token de ativação enviado por email
    """
    try:
        request = VerificarTokenRequest.model_validate(
            flask_request.get_json()
        )
        repository = MembrosRepository(database)
        usecase = VerificarTokenAtivacaoContaUseCase(repository)
        return usecase.execute(request), HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@autenticacao_bp.post('/ativacao-de-conta')
@swagger.validate(
    json=AtivarContaRequest,
    query=UsarHttpOnlyQuery,
    tags=['Autenticação'],
)
def ativacao_de_conta():
    """
    Realiza ativação da conta
    """
    try:
        request = AtivarContaRequest.model_validate(flask_request.get_json())
        query = UsarHttpOnlyQuery.model_validate(flask_request.args.to_dict())
        repository = MembrosRepository(database)
        usecase = AtivarContaUseCase(repository)
        response = usecase.execute(request, query)
        return response
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@autenticacao_bp.get('/verificar-cadastro-por-email/<email>')
@swagger.validate(
    resp=Response(HTTP_500=ErroPadraoResponse, HTTP_200=ResponsePadraoSchema),
    tags=['Autenticação'],
)
def busca_cadastro_por_email(email):
    try:
        notification = SendGridService()
        repository = MembrosRepository(database)
        usecase = BuscaCadastroPorEmail(repository, notification)
        usecase.execute(email)
        return {'msg': 'Cadastro encontrado com sucesso'}, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@autenticacao_bp.get('/usuario-logado')
@swagger.validate(
    resp=Response(HTTP_200=UsuarioLogadoResponse, HTTP_500=ErroPadraoResponse),
    tags=['Autenticação'],
)
@jwt_required()
def usuario_logado():
    """
    Retorna as informações do usuário logado.
    """
    try:
        usecase = UsuarioLogadoUseCase()
        return usecase.execute(), HTTPStatus.OK
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@autenticacao_bp.post('/recuperar-senha')
@swagger.validate(
    json=RecuperarSenhaRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    security={},
    tags=['Autenticação'],
)
def post_forgot_password():
    """Envia um email para recuperar a senha da conta"""
    try:
        repository = AutenticacaoRepository(database)
        notification = SendGridService()
        controller = RecuperarSenhaUseCase(repository, notification)
        request = RecuperarSenhaRequest.model_validate(flask_request.json)
        controller.execute(request)

        return {'msg': 'Email enviado com sucesso.'}, HTTPStatus.OK

    except Exception as err:
        error_response = errors_handler(err)
        return error_response


@autenticacao_bp.post('/nova-senha')
@swagger.validate(
    query=NovaSenhaQuery,
    json=NovaSenhaRequest,
    resp=Response(HTTP_200=ResponsePadraoSchema, HTTP_500=ErroPadraoResponse),
    security={},
    path_parameter_descriptions={
        'token': 'Token enviado por email para alterar a senha'
    },
    tags=['Autenticação'],
)
def nova_senha():
    """Altera a senha do usuário deslogado"""
    try:
        membro_repository = MembrosRepository(database)
        controller = NovaSenhaUseCase(membro_repository)
        request = NovaSenhaRequest.model_validate(flask_request.json)
        query_params = NovaSenhaQuery.model_validate(
            flask_request.args.to_dict()
        )
        controller.execute(request, query_params)
        return {'msg': 'Senha alterada com sucesso.'}, HTTPStatus.OK
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@autenticacao_bp.post('/alterar-senha')
@swagger.validate(
    json=AlterarSenhaRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Autenticação'],
)
@jwt_required()
def alterar_senha():
    """
    Altera a senha do usuário logado
    """
    try:
        repository = AutenticacaoRepository(database)
        controller = AlterarSenhaUseCase(repository)
        request = AlterarSenhaRequest.model_validate(flask_request.json)
        controller.execute(request)
        return {'msg': 'Senha alterada com sucesso.'}, HTTPStatus.OK
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response
