from abc import ABC, abstractmethod
from typing import Optional

from flask_sqlalchemy import SQLAlchemy


from models.clifor import Clifor
from models.schemas.users.post.register_brazilian_user_with_address import (
    RegisterBrazilianUserWithAddressRequest,
)
from models.schemas.users.post.register_user_full import (
    RegisterUserFullFormData,
)
from models.usuario import Usuario
from services.file_service import FileService


class RegisterDeletedUserInterface(ABC):

    @abstractmethod
    def register(
        self,
        database: SQLAlchemy,
        usuario: Usuario,
        clifor: Clifor,
        pais: str,
        nome: str,
        email: str,
        password: str,
        campanha_origem: Optional[int],
    ):
        pass


class RegisterDeletedUserFullInterface(ABC):
    @abstractmethod
    def register(
        self,
        database: SQLAlchemy,
        file_service: FileService,
        usuario=Usuario,
        clifor=Clifor,
        request=RegisterUserFullFormData,
    ):
        pass


class RegisterDeletedBrazilianUserWithAddressInterface(ABC):
    @abstractmethod
    def register(
        self,
        database: SQLAlchemy,
        usuario=Usuario,
        clifor=Clifor,
        request=RegisterBrazilianUserWithAddressRequest,
    ):
        pass
