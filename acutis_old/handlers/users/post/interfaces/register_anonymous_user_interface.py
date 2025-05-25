from abc import ABC, abstractmethod
from typing import Optional

from flask_sqlalchemy import SQLAlchemy


from models.clifor import Clifor
from models.perfil import Perfil
from models.schemas.users.post.register_brazilian_user_with_address import (
    RegisterBrazilianUserWithAddressRequest,
)
from models.schemas.users.post.register_user_full import (
    RegisterUserFullFormData,
)
from services.file_service import FileService


class RegisterAnonymousUserInterface(ABC):
    @abstractmethod
    def register(
        self,
        database: SQLAlchemy,
        clifor: Clifor,
        profile: Perfil,
        pais: str,
        nome: str,
        email: str,
        password: str,
        numero_documento: str,
        campanha_origem: Optional[int],
        origem_cadastro: Optional[int],
    ):
        pass


class RegisterAnonymousUserFullInterface(ABC):
    @abstractmethod
    def register(
        self,
        database: SQLAlchemy,
        file_service: FileService,
        clifor: Clifor,
        perfil: Perfil,
        request: RegisterUserFullFormData,
        origem_cadastro: Optional[int],
    ):
        pass


class RegisterAnonymousBrazilianUserWithAddressInterface(ABC):
    @abstractmethod
    def register(
        self,
        database=SQLAlchemy,
        clifor=Clifor,
        perfil=Perfil,
        origem_cadastro=Optional[int],
        request=RegisterBrazilianUserWithAddressRequest,
    ):
        pass
