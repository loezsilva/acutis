import os
import urllib
from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy import StaticPool

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
URL_FRONTEND_DOE = os.environ.get("URL_FRONTEND_DOE")
URL_FRONTEND_CADASTRO = os.environ.get("URL_FRONTEND_CADASTRO")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
EMAIL = os.environ.get("MAIL_USERNAME")
MAXIPAGO_URL_API = os.environ.get("MAXIPAGO_URL_API")
MAXIPAGO_URL_XML = os.environ.get("MAXIPAGO_URL_XML")
MAXIPAGO_URL_REPORTS_API = os.environ.get("MAXIPAGO_URL_REPORTS_API")
ACCOUNT_NAME = os.environ.get("ACCOUNT_NAME")
ACCOUNT_KEY = os.environ.get("ACCOUNT_KEY")
ACCOUNT_PRIVATE_CONTAINER = os.environ.get("ACCOUNT_PRIVATE_CONTAINER")
ACCOUNT_PUBLIC_CONTAINER = os.environ.get("ACCOUNT_PUBLIC_CONTAINER")
ITAU_URL_AUTH = os.environ.get("ITAU_URL_AUTH")
ITAU_URL_PIX = os.environ.get("ITAU_URL_PIX")
ITAU_URL_BOLETO = os.environ.get("ITAU_URL_BOLETO")
ITAU_URL_BOLECODE = os.environ.get("ITAU_URL_BOLECODE")
ITAU_PIX_CLIENT_ID = os.environ.get("ITAU_PIX_CLIENT_ID")
ITAU_PIX_CLIENT_SECRET = os.environ.get("ITAU_PIX_CLIENT_SECRET")
ITAU_BOLETO_CLIENT_ID = os.environ.get("ITAU_BOLETO_CLIENT_ID")
ITAU_BOLETO_CLIENT_SECRET = os.environ.get("ITAU_BOLETO_CLIENT_SECRET")
MERCADO_PAGO_ACCESS_TOKEN = os.environ.get("PROD_MERCADO_PAGO_ACCESS_TOKEN")
MERCADO_PAGO_SECRET_KEY = os.environ.get("MERCADO_PAGO_SECRET_KEY")
CHAVE_PIX_HESED = os.environ.get("CHAVE_PIX_HESED")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
ENVIRONMENT = os.environ.get("ENVIRONMENT", None)

BLACKLIST = set()


class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SCHEDULER_API_ENABLED = False

    @staticmethod
    def init_app(app):
        pass


class DatabaseConfig(Config):
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
    DATABASE_PASSWORD = urllib.parse.quote_plus(os.environ.get("SA_PASSWORD"))
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_BIND = os.environ.get("BIND_DATABASE_NAME")

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL},{DATABASE_PORT}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_BINDS = {
        "enderecos": {
            "url": f"mssql+pyodbc://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_URL},{DATABASE_PORT}/Enderecos?driver=ODBC+Driver+17+for+SQL+Server",
            "pool_size": 100,
            "max_overflow": -1,
            "pool_timeout": 30,
        }
    }

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 100,
        "max_overflow": -1,
        "pool_timeout": 30,
    }


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_BINDS = {"enderecos": "sqlite:///:memory:"}
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
