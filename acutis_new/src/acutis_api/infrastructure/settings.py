from datetime import timedelta
from urllib.parse import quote_plus

from flask import Flask
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    ENVIRONMENT: str | None = 'desenvolvimento'
    URL_FRONTEND_DOE: str | None = None
    URL_FRONTEND_CADASTRO: str | None = None
    SECRET_KEY: str | None = None
    JWT_SECRET_KEY: str | None = None
    JWT_COOKIE_SECURE: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_COOKIE_SAMESITE: str = 'Strict'

    DATABASE_HOST: str | None = None
    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_NAME: str | None = None
    DATABASE_PORT: int | None = 1433
    BIND_DATABASE_NAME: str | None = None

    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None

    SENDGRID_API_KEY: str | None = None
    SENDGRID_EMAIL: str | None = None

    MAXIPAGO_URL_XML: str | None = None
    MAXIPAGO_URL_API: str | None = None
    MAXIPAGO_URL_REPORTS_API: str | None = None
    MAXIPAGO_MERCHANT_ID: str | None = None
    MAXIPAGO_MERCHANT_KEY: str | None = None

    ITAU_AUTH_URL: str | None = None
    ITAU_PIX_URL: str | None = None
    ITAU_BOLETO_URL: str | None = None
    ITAU_BOLECODE_URL: str | None = None
    ACUTIS_WEBHOOK_ITAU_URL: str | None = None
    ITAU_PIX_CLIENT_ID: str | None = None
    ITAU_PIX_CLIENT_SECRET: str | None = None
    ITAU_BOLETO_CLIENT_ID: str | None = None
    ITAU_BOLETO_CLIENT_SECRET: str | None = None

    MERCADO_PAGO_ACCESS_TOKEN: str | None = None
    MERCADO_PAGO_SECRET_KEY: str | None = None

    CLOUDFLARE_API_KEY: str | None = None
    CLOUDFLARE_EMAIL: str | None = None

    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str | None = None
    AWS_BUCKET_NAME: str | None = None

    GOOGLE_MAPS_API_KEY: str | None = None
    URL_FRONTEND_DOE: str | None = None
    URL_FRONTEND_CADASTRO: str | None = None
    MAILHOG_HOST: str | None = None
    MAILHOG_PORT: str | None = None


settings = Settings()


class Config:
    GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
    SECRET_KEY = settings.SECRET_KEY

    JWT_SECRET_KEY = settings.JWT_SECRET_KEY
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = settings.JWT_COOKIE_SECURE
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_IN_COOKIES = True
    JWT_COOKIE_SAMESITE = settings.JWT_COOKIE_SAMESITE
    JWT_REFRESH_COOKIE_PATH = '/autenticacao/refresh'

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    SQLALCHEMY_BINDS = {
        'enderecos': f'mssql+pyodbc://{settings.DATABASE_USERNAME}:{quote_plus(settings.DATABASE_PASSWORD)}@{settings.DATABASE_HOST},{settings.DATABASE_PORT}/{settings.BIND_DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app: Flask):
        pass  # pragma: no cover


class ApplicationConfig(Config):
    DATABASE_PASSWORD = quote_plus(settings.DATABASE_PASSWORD)

    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{settings.DATABASE_USERNAME}:{DATABASE_PASSWORD}@{settings.DATABASE_HOST},{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server'

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 100,
        'max_overflow': -1,
        'pool_timeout': 30,
    }


class TestingConfig(Config):
    @classmethod
    def set_test_config(cls, database_url):
        cls.TESTING = True
        database_url += '?driver=ODBC+Driver+17+for+SQL+Server'
        cls.SQLALCHEMY_DATABASE_URI = database_url
        settings.ENVIRONMENT = 'teste'
