from faker import Faker
import pytest

from models.actions_leads import ActionsLeads
from models.clifor import Clifor
from models.foto_leads import FotoLeads
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.users_imports import UsersImports
from models.usuario import Usuario
from utils.functions import get_current_time
from builder import db
from utils.tests.datamaker import (
    address_maker,
    clifor_maker,
    user_maker,
    user_permission_maker,
)

faker = Faker("pt_BR")


@pytest.fixture
def seed_register_deleted_user():
    usuario = Usuario(
        nome="usuario test",
        status=False,
        email="testeemail@institutohesed.org.br",
        deleted_at=get_current_time(),
        password="1234@1234",
    )
    db.session.add(usuario)
    db.session.flush()

    clifor = Clifor(
        fk_usuario_id=usuario.id,
        nome="usuario test",
        cpf_cnpj="65335887028",
        email="testeemail@institutohesed.org.br",
    )
    db.session.add(clifor)
    db.session.commit()

    perfil = Perfil.query.filter(Perfil.nome.ilike("Administrador")).first()

    permissao_usuario = PermissaoUsuario(
        fk_usuario_id=usuario.id,
        fk_perfil_id=perfil.id,
        usuario_criacao=0,
    )
    db.session.add(permissao_usuario)
    db.session.commit()

    return permissao_usuario


@pytest.fixture
def seed_register_anonymous_user():
    clifor = Clifor(nome="Yan o brabo", cpf_cnpj="15718702000182")
    db.session.add(clifor)
    db.session.commit()

    return


@pytest.fixture
def seed_user_active_account():
    user = Usuario(nome="testuser", email="testuser@example.com", status=False)
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def seed_new_lead_action():
    action = ActionsLeads(
        nome="Campanha Teste",
        status=True,
        preenchimento_foto=True,
    )
    db.session.add(action)
    db.session.commit()
    return action


@pytest.fixture
def seed_new_lead_already_registered():
    action = ActionsLeads(
        nome="Campanha Teste",
        status=True,
        preenchimento_foto=True,
    )
    db.session.add(action)
    db.session.flush()

    lead = UsersImports(
        nome="Usuário Antigo",
        email="teste@headers.com.br",
        phone="11987654321",
        intencao="Intenção antiga",
        origem_cadastro=action.id,
        data_criacao=get_current_time(),
    )
    db.session.add(lead)
    db.session.flush()

    photo_lead = FotoLeads(
        fk_user_import_id=lead.id,
        fk_action_lead_id=action.id,
        foto="foto_antiga.jpg",
        data_download=get_current_time(),
        user_download=1,
    )
    db.session.add(photo_lead)
    db.session.commit()

    return lead, photo_lead


@pytest.fixture
def seed_register_deleted_user_full_data():
    usuario = user_maker()
    usuario.email = "debora-vieira72@hotmail.com"
    usuario.deleted_at = get_current_time()
    db.session.add(usuario)
    db.session.flush()

    clifor = clifor_maker(usuario.id)
    clifor.cpf_cnpj = "37000086270"
    clifor.email = "debora-vieira72@hotmail.com"
    db.session.add(clifor)
    db.session.flush()

    endereco = address_maker(clifor.id)
    db.session.add(endereco)

    perfil = Perfil.query.filter_by(nome="Administrador").first()

    permissao_usuario = user_permission_maker(usuario.id, perfil.id)
    db.session.add(permissao_usuario)
    db.session.commit()

    return
