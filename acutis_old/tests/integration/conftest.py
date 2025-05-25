from faker import Faker
import pytest

from models.clifor import Clifor
from models.endereco import Endereco
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from builder import db
from utils.functions import get_current_time

from flask_jwt_extended import create_access_token

from models.permissao_menu import PermissaoMenu
from models.menu_sistema import MenuSistema
from main import create_app

faker = Faker("pt_BR")


@pytest.fixture(scope="session")
def test_client():
    client = create_app("config.TestingConfig")
    client.testing = True

    with client.test_client() as testing_client:
        with client.app_context():
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="session", autouse=True)
def clean_db(test_client):
    db.create_all()


@pytest.fixture(scope="session", autouse=True)
def seed_data_profile(clean_db):
    profiles = [
        {
            "nome": "Administrador",
            "status": 1,
            "super_perfil": 1,
            "usuario_criacao": 0,
        },
        {
            "nome": "Benfeitor",
            "status": 1,
            "super_perfil": 0,
            "usuario_criacao": 0,
        },
        {
            "nome": "Operacional",
            "status": 1,
            "super_perfil": 1,
            "usuario_criacao": 0,
        },
        {
            "nome": "Campanhas e LP",
            "status": 1,
            "super_perfil": 1,
            "usuario_criacao": 0,
        },
        {
            "nome": "Marketing",
            "status": 1,
            "super_perfil": 1,
            "usuario_criacao": 0,
        },
        {
            "nome": "Voluntario Agape",
            "status": 1,
            "super_perfil": 1,
            "usuario_criacao": 0,
        },
        {
            "nome": "Administrador Agape",
            "status": 1,
            "super_perfil": 1,
            "usuario_criacao": 0,
        },
    ]

    profiles_db = [Perfil(**profile) for profile in profiles]
    db.session.add_all(profiles_db)
    db.session.commit()

    return profiles_db


@pytest.fixture(scope="session", autouse=True)
def seed_data_systems_menu(seed_data_profile):
    perfis = seed_data_profile
    menus = [
        {"slug": "campanha", "menu": "Campanhas", "usuario_criacao": 1},
        {"slug": "usuario", "menu": "Usuários", "usuario_criacao": 1},
        {"slug": "perfil", "menu": "Perfis de acesso", "usuario_criacao": 1},
        {
            "slug": "dash_board_users",
            "menu": "DashBoard de usuários",
            "usuario_criacao": 1,
        },
        {
            "slug": "dash_board_donations",
            "menu": "DashBoard de doações",
            "usuario_criacao": 1,
        },
        {"slug": "endereco", "menu": "Endereços", "usuario_criacao": 1},
        {"slug": "doacoes", "menu": "Doações", "usuario_criacao": 1},
        {"slug": "logs", "menu": "Listagem de Logs", "usuario_criacao": 1},
        {"slug": "gateway", "menu": "Gateway", "usuario_criacao": 1},
        {"slug": "general", "menu": "Generais", "usuario_criacao": 1},
        {"slug": "mensageria", "menu": "Mensageria", "usuario_criacao": 1},
        {
            "slug": "familia_agape",
            "menu": "Família Ágape",
            "usuario_criacao": 1,
        },
        {
            "slug": "doacao_agape",
            "menu": "Doação Ágape",
            "usuario_criacao": 1,
        },
        {
            "slug": "estoque_agape",
            "menu": "Estoque Ágape",
            "usuario_criacao": 1,
        },
        {
            "slug": "acao_doacao_agape",
            "menu": "Ação Doação Ágape",
            "usuario_criacao": 1,
        },
        {
            "slug": "vocacional_masculino",
            "menu": "Vocacional Masculino",
            "usuario_criacao": 1,
        },
        {
            "slug": "vocacional_feminino",
            "menu": "Vocacional Feminino",
            "usuario_criacao": 1,
        },
    ]

    for menu in menus:
        novo_menu = MenuSistema(**menu)
        db.session.add(novo_menu)
        db.session.flush()

        for perfil in perfis:
            permissoes = {
                "fk_perfil_id": perfil.id,
                "fk_menu_id": novo_menu.id,
                "acessar": 0,
                "criar": 0,
                "editar": 0,
                "deletar": 0,
                "usuario_criacao": menu["usuario_criacao"],
            }
            if perfil.nome.lower() == "administrador":
                permissoes["acessar"] = 1
                permissoes["criar"] = 1
                permissoes["editar"] = 1
                permissoes["deletar"] = 1

            permissao_menu = PermissaoMenu(**permissoes)
            db.session.add(permissao_menu)

        db.session.commit()


@pytest.fixture(scope="session", autouse=True)
def seed_payment_type_data(seed_data_systems_menu):
    payments_types = [
        {"descricao": "Credito", "usuario_criacao": 0},
        {"descricao": "Pix", "usuario_criacao": 0},
        {"descricao": "Boleto", "usuario_criacao": 0},
    ]

    payment_type_db = [
        FormaPagamento(**payment_type) for payment_type in payments_types
    ]
    db.session.add_all(payment_type_db)
    db.session.commit()


@pytest.fixture(scope="session")
def seed_admin_user_token():
    user = Usuario(
        nome="adminuser",
        email="adminuser@headers.com.br",
        avatar="admin_foto.png",
    )
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(
        nome="adminuser",
        data_nascimento=get_current_time().date(),
        telefone1="42987220864",
        email="adminuser@headers.com.br",
        fk_usuario_id=user.id,
        usuario_criacao=user.id,
    )
    db.session.add(clifor)
    db.session.flush()

    address = Endereco(fk_clifor_id=clifor.id, usuario_criacao=user.id)
    db.session.add(address)

    perfil = Perfil.query.filter_by(nome="Administrador").first()

    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id, fk_perfil_id=perfil.id, usuario_criacao=user.id
    )
    db.session.add(user_permission)
    db.session.commit()

    token = create_access_token(identity=user.id)

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def seed_user_with_dependencies():
    nome = faker.name()
    email = faker.email(domain="headers.com.br")
    cpf = faker.cpf()
    user = Usuario(
        nome=nome,
        email=email,
        country="brasil",
        password="SenhaAntiga123",
        status=True,
    )
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(
        fk_usuario_id=user.id,
        nome=nome,
        email=email,
        cpf_cnpj=cpf,
        telefone1="11987654321",
        data_nascimento=get_current_time().date(),
        usuario_criacao=0,
    )
    db.session.add(clifor)
    db.session.flush()

    address = Endereco(fk_clifor_id=clifor.id, usuario_criacao=user.id)
    db.session.add(address)

    perfil = Perfil.query.filter_by(nome="Benfeitor").first()

    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id, fk_perfil_id=perfil.id, usuario_criacao=0
    )
    db.session.add(user_permission)

    forma_pagamento = FormaPagamento.query.filter_by(descricao="Pix").first()

    pedido = Pedido(
        fk_clifor_id=clifor.id,
        anonimo=False,
        fk_forma_pagamento_id=forma_pagamento.id,
        periodicidade=1,
        usuario_criacao=0,
    )
    db.session.add(pedido)
    db.session.commit()

    return user, clifor, address, pedido
