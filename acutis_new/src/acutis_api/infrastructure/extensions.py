from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from spectree import SecurityScheme, SpecTree

from acutis_api.domain.database import table_registry

BLACKLIST = set()

cors = CORS()
database = SQLAlchemy(
    metadata=table_registry.metadata, session_options={'autoflush': False}
)
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, storage_uri='memory://')
migrate = Migrate()
oauth = OAuth()
swagger = SpecTree(
    'flask',
    title='Instituto HeSed - Acutis API',
    path='api/docs',
    version='0.0.1',
    security_schemes=[
        SecurityScheme(
            name='api_key',
            data={'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
        )
    ],
    security={'api_key': []},
)


def configure_extensions(app: Flask):
    from acutis_api.domain.entities.benfeitor import Benfeitor as Benfeitor

    cors.init_app(app, supports_credentials=True)
    database.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, database)
    oauth.init_app(app)


__all__ = [
    'database',
    'limiter',
    'jwt',
    'oauth',
    'swagger',
    'configure_extensions',
]
