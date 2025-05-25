from faker import Faker
import pytest
from builder import db
from models.clifor import Clifor
from models.endereco import Endereco
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from utils.functions import get_current_time

faker = Faker("pt_BR")


@pytest.fixture
def seed_benefector_user():
    nome = faker.name()
    email = faker.email(domain="headers.com.br")
    user = Usuario(
        nome=nome,
        email=email,
        avatar="avatar.jpg",
    )
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(
        nome=nome,
        fk_usuario_id=user.id,
        usuario_criacao=user.id,
        data_nascimento=get_current_time().date(),
    )
    db.session.add(clifor)
    db.session.flush()

    address = Endereco(fk_clifor_id=clifor.id, usuario_criacao=user.id)
    db.session.add(address)

    perfil = Perfil.query.filter_by(nome="Benfeitor").first()

    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id, fk_perfil_id=perfil.id, usuario_criacao=user.id
    )
    db.session.add(user_permission)
    db.session.commit()

    return user
