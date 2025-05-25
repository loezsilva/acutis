from http import HTTPStatus
import io
from faker import Faker
from flask.testing import FlaskClient
from builder import db

faker = Faker("pt-BR")


def test_update_agape_member_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_member,
):
    membro = seed_agape_member

    foto_documento = (io.BytesIO(b'simulando_imagem'), 'filename.png')

    payload = {
        "cpf": "94805026073",
        "data_nascimento": "1987-06-24",
        "email": "lionelmessi@gmail.com",
        "escolaridade": "Ensino Médio Incompleto",
        "funcao_familiar": "Pai",
        "nome": "Lionel Messi",
        "ocupacao": "Jogador de Futebol",
        "renda": 100_000_000.00,
        "responsavel": False,
        "telefone": "6737713531",
        "beneficiario_assistencial": True,
        "foto_documento": foto_documento,
    }

    response = test_client.put(
        f"/agape/editar-membro/{membro.id}",
        data=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"msg": "Membro atualizado com sucesso."}

    db.session.refresh(membro)

    assert membro.cpf == payload["cpf"]
    assert (
        membro.data_nascimento.strftime("%Y-%m-%d")
        == payload["data_nascimento"]
    )
    assert membro.email == payload["email"]
    assert membro.escolaridade == payload["escolaridade"]
    assert membro.funcao_familiar == payload["funcao_familiar"]
    assert membro.nome == payload["nome"]
    assert membro.ocupacao == payload["ocupacao"]
    assert membro.renda == payload["renda"]
    assert membro.responsavel == payload["responsavel"]
    assert membro.telefone == payload["telefone"]


def test_update_agape_member_error_responsibly_without_cpf(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_member
):
    membro = seed_agape_member

    payload = {
        "data_nascimento": "1987-06-24",
        "email": "lionelmessi@gmail.com",
        "escolaridade": "Ensino Médio Incompleto",
        "funcao_familiar": "Pai",
        "nome": "Lionel Messi",
        "ocupacao": "Jogador de Futebol",
        "renda": 100_000_000.00,
        "responsavel": True,
        "telefone": "6737713531",
        "beneficiario_assistencial": True,
    }

    response = test_client.put(
        f"/agape/editar-membro/{membro.id}",
        data=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "error": f"O CPF do responsável {payload['nome']} é obrigatório."
    }


def test_update_agape_member_error_member_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
):
    payload = {
        "cpf": "94805026073",
        "data_nascimento": "1987-06-24",
        "email": "lionelmessi@gmail.com",
        "escolaridade": "Ensino Médio Incompleto",
        "funcao_familiar": "Pai",
        "nome": "Lionel Messi",
        "ocupacao": "Jogador de Futebol",
        "renda": 100_000_000.00,
        "responsavel": False,
        "telefone": "6737713531",
        "beneficiario_assistencial": True,
    }

    response = test_client.put(
        "/agape/editar-membro/9999",
        data=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Membro não encontrado."}


def test_update_agape_member_error_cpf_already_exists(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_member,
    seed_agape_family_with_members,
):
    membro = seed_agape_member
    _, membros = seed_agape_family_with_members

    payload = {
        "cpf": membros[0].cpf,
        "data_nascimento": "1987-06-24",
        "email": "lionelmessi@gmail.com",
        "escolaridade": "Ensino Médio Incompleto",
        "funcao_familiar": "Pai",
        "nome": "Lionel Messi",
        "ocupacao": "Jogador de Futebol",
        "renda": 100_000_000.00,
        "responsavel": False,
        "telefone": "6737713531",
        "beneficiario_assistencial": True,
    }

    response = test_client.put(
        f"/agape/editar-membro/{membro.id}",
        data=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Ja existe um membro com o CPF {membros[0].cpf} cadastrado."
    }


def test_update_agape_member_error_email_already_exists(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_member,
    seed_agape_family_with_members,
):
    membro = seed_agape_member
    _, membros = seed_agape_family_with_members

    payload = {
        "cpf": faker.cpf(),
        "data_nascimento": "1987-06-24",
        "email": membros[0].email,
        "escolaridade": "Ensino Médio Incompleto",
        "funcao_familiar": "Pai",
        "nome": "Lionel Messi",
        "ocupacao": "Jogador de Futebol",
        "renda": 100_000_000.00,
        "responsavel": False,
        "telefone": "6737713531",
        "beneficiario_assistencial": True,
    }

    response = test_client.put(
        f"/agape/editar-membro/{membro.id}",
        data=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Ja existe um membro com o email {membros[0].email} cadastrado."
    }
