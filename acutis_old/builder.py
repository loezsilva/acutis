from http import HTTPStatus

import sentry_sdk
from flask import Flask
from flask import Response as FlaskResponse
from flask import request
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from spectree import Response, SecurityScheme, SpecTree
from translate import Translator

from config import BLACKLIST, ENVIRONMENT
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_forbidden import ForbiddenError
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unauthorized import UnauthorizedError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from services.factories import file_service_factory
from utils.response import DefaultResponseSchema

api = SpecTree(
    "flask",
    title="Instituto HeSed - Acutis API",
    version="0.15.2",
    path="apidocs",
    security_schemes=[
        SecurityScheme(
            name="api_key",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )
    ],
    security={"api_key": []},
)

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
translator = Translator(to_lang="pt-br")
scheduler = APScheduler()
migrate = Migrate()
jwt = JWTManager()
db = SQLAlchemy()


if ENVIRONMENT == "production":
    sentry_sdk.init(
        dsn="https://2b7f138d14428d3588dc79d92900e487@o4508708469407744.ingest.us.sentry.io/4508708492345344",
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
        ignore_errors=[
            BadRequestError,
            UnauthorizedError,
            ForbiddenError,
            NotFoundError,
            ConflictError,
            HttpUnprocessableEntity,
        ],
    )


def create_app(config_class: object | str):
    app = Flask(__name__)

    from controllers import (
        address_controller,
        admin_controller,
        agape_controller,
        auth_controller,
        campaign_controller,
        checkout_controller,
        dash_board,
        dash_board_donations,
        group_controller,
        image_controller,
        landpage_controller,
        log_controller,
        payment_gateway_controller,
        pedidos_de_oracao,
        services_controller,
        user_controller,
        webhooks_controller,
        youtube_lives_controller,
        mensageria_controller,
        vocacional_controller
    )
    from models import (
        CargoUsuario,
        MenuSistema,
        Perfil,
        PermissaoMenu,
        PermissaoUsuario,
        Usuario,
    )

    @app.get("/")
    @api.validate(
        resp=Response(HTTP_200=DefaultResponseSchema), tags=["Página Inicial"]
    )
    def hello_hesed():
        """
        Hello HeSed
        """
        return {"msg": "Hello HeSed!"}

    @app.errorhandler(429)
    def many_requests(error):
        return {
            "error": "Muitas requisições. Aguarde alguns segundos antes de enviar uma nova requisição."
        }, 429

    CORS(app, supports_credentials=True)

    app.config.from_object(config_class)

    jwt.init_app(app)

    db.init_app(app)

    scheduler.init_app(app)

    limiter.init_app(app)

    from schedules import (
        job_atualiza_status_campanha,
        job_atualiza_status_pagamento_48_horas,
        job_dispara_email_recorrencia_pagamento_pix_boleto,
        job_obriga_atualizar_endereco,
    )

    if ENVIRONMENT == "production":
        scheduler.start()

    migrate.init_app(app, db)

    @app.before_request
    def protect_docs():
        return
        if request.path.startswith("/apidocs"):
            auth = request.authorization
            if auth:
                user = Usuario.query.filter_by(email=auth.username).first()
                if user and user.verify_password(auth.password):
                    permissao = (
                        db.session.query(
                            Perfil.nome,
                        )
                        .select_from(Usuario)
                        .join(
                            PermissaoUsuario,
                            Usuario.id == PermissaoUsuario.fk_usuario_id,
                        )
                        .join(
                            Perfil, Perfil.id == PermissaoUsuario.fk_perfil_id
                        )
                        .filter(Usuario.id == user.id)
                        .scalar()
                    )

                    if permissao.lower() == "administrador":
                        return

            return FlaskResponse(
                "Acesso negado: Forneça um nome de usuário e senha válidos.",
                status=HTTPStatus.UNAUTHORIZED,
                headers={"WWW-Authenticate": "Basic realm='Login Required'"},
            )

    @jwt.expired_token_loader
    def expired_token(header, payload):
        return {"msg": "Token expirado."}, 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        return {"msg": "Token inválido."}, 401

    @jwt.revoked_token_loader
    def revoked_token(header, payload):
        return {
            "msg": "Você foi deslogado. Por favor, faça o login novamente."
        }, 401

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(header, payload):
        jti = payload["jti"]
        return jti in BLACKLIST

    @jwt.user_lookup_loader
    def user_load(header, payload):
        fk_usuario_id = payload["sub"]

        result = Usuario.get_informations_current_user(fk_usuario_id)

        avatar = None

        file_service = file_service_factory()

        if result.avatar is not None:

            avatar = file_service.get_public_url(result.avatar)

        permissoes = (
            db.session.query(
                PermissaoMenu.fk_menu_id,
                PermissaoMenu.acessar,
                PermissaoMenu.criar,
                PermissaoMenu.editar,
                PermissaoMenu.deletar,
                MenuSistema.slug,
            )
            .select_from(PermissaoMenu)
            .join(MenuSistema, PermissaoMenu.fk_menu_id == MenuSistema.id)
            .filter(PermissaoMenu.fk_perfil_id == result.fk_perfil_id)
            .all()
        )

        cargo = (
            db.session.query(CargoUsuario.fk_cargo_id.label("id"))
            .filter(
                CargoUsuario.fk_usuario_id == result.id,
                CargoUsuario.convite != 2,
                CargoUsuario.convite != 3,
            )
            .first()
        )

        current_user = {
            "id": result.id,
            "nome": result.nome,
            "nome_social": result.nome_social,
            "email": result.email,
            "numero_documento": result.cpf_cnpj,
            "data_nascimento": (
                result.data_nascimento.strftime("%d/%m/%Y")
                if result.data_nascimento
                else None
            ),
            "telefone": result.telefone1,
            "sexo": result.sexo,
            "avatar": avatar,
            "pais": result.country,
            "fk_perfil_id": result.fk_perfil_id,
            "nome_perfil": result.nome_perfil,
            "fk_clifor_id": result.fk_clifor_id,
            "obriga_atualizar_endereco": result.obriga_atualizar_endereco,
            "obriga_atualizar_cadastro": result.obriga_atualizar_cadastro,
            "campanha_origem": result.campanha_origem,
            "cargo_id": cargo.id if cargo else None,
            "super_perfil": result.super_perfil,
            "permissoes": {
                permissao.slug: {
                    "menu_id": permissao.fk_menu_id,
                    "acessar": permissao.acessar,
                    "criar": permissao.criar,
                    "editar": permissao.editar,
                    "deletar": permissao.deletar,
                }
                for permissao in permissoes
            },
        }

        return current_user

    blueprints = [
        admin_controller,
        agape_controller,
        auth_controller,
        campaign_controller,
        checkout_controller,
        dash_board_donations,
        dash_board,
        address_controller,
        payment_gateway_controller,
        log_controller,
        group_controller,
        image_controller,
        landpage_controller,
        pedidos_de_oracao,
        services_controller,
        user_controller,
        webhooks_controller,
        youtube_lives_controller,
        mensageria_controller,
        vocacional_controller
    ]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    if ENVIRONMENT != "production":
        api.register(app)

    return app
