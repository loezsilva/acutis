from typing import Optional
from faker import Faker

from models.clifor import Clifor
from models.endereco import Endereco
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario


faker = Faker("pt_BR")


def user_maker() -> Usuario:
    return Usuario(
        nome=faker.name(),
        nome_social=faker.name(),
        email=faker.email(domain="hotmail.com"),
    )


def clifor_maker(user_id: Optional[int]) -> Clifor:
    return Clifor(fk_usuario_id=user_id)


def address_maker(clifor_id: int) -> Endereco:
    return Endereco(fk_clifor_id=clifor_id)


def user_permission_maker(user_id: int, perfil_id: int) -> PermissaoUsuario:
    return PermissaoUsuario(
        fk_usuario_id=user_id, fk_perfil_id=perfil_id, usuario_criacao=0
    )
