import pytest
from faker import Faker

from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from builder import db


@pytest.fixture
def seed_test_delete_profile():
    faker = Faker()
    user = Usuario(
        nome=faker.name(),
        status=True,
        email=faker.email(),
    )
    db.session.add(user)
    db.session.flush()

    profile = Perfil(
        nome="Testing",
        status=True,
        super_perfil=False,
        usuario_criacao=0,
    )
    db.session.add(profile)
    db.session.flush()

    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id,
        fk_perfil_id=profile.id,
        usuario_criacao=0,
    )
    db.session.add(user_permission)
    db.session.commit()

    return user_permission, profile
