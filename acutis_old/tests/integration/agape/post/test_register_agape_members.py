from http import HTTPStatus
from flask.testing import FlaskClient


def test_register_agape_members_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family
):
    _, familia = seed_agape_family

    payload = {
        "membros": [
            {
                "cpf": "20438928512",
                "data_nascimento": "2001-01-07",
                "email": "jorge_nascimento@policiamilitar.sp.gov.br",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Jorge Paulo Gabriel Nascimento",
                "ocupacao": "Policial Militar",
                "renda": 5000.00,
                "responsavel": True,
                "telefone": "(73) 3901-9965",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "2024-01-17",
                "escolaridade": "Créche",
                "funcao_familiar": "Filho",
                "nome": "Lucca Lucca Lima",
                "ocupacao": "Neném",
                "renda": 0.00,
                "responsavel": False,
                "beneficiario_assistencial": False,
            },
        ]
    }

    response = test_client.post(
        f"/agape/cadastrar-membros/{familia.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Membros cadastrados com sucesso."}


def test_register_agape_members_error_responsible_without_cpf(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family
):
    _, familia = seed_agape_family

    payload = {
        "membros": [
            {
                "data_nascimento": "2001-01-07",
                "email": "jorge_nascimento@policiamilitar.sp.gov.br",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Jorge Paulo Gabriel Nascimento",
                "ocupacao": "Policial Militar",
                "renda": 5000.00,
                "responsavel": True,
                "telefone": "(73) 3901-9965",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "2024-01-17",
                "escolaridade": "Créche",
                "funcao_familiar": "Filho",
                "nome": "Lucca Lucca Lima",
                "ocupacao": "Neném",
                "renda": 0.00,
                "responsavel": False,
                "beneficiario_assistencial": True,
            },
        ]
    }

    response = test_client.post(
        f"/agape/cadastrar-membros/{familia.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "error": f"O CPF do responsável {payload['membros'][0]['nome']} é obrigatório."
    }


def test_register_agape_members_error_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {
        "membros": [
            {
                "data_nascimento": "2001-01-07",
                "email": "jorge_nascimento@policiamilitar.sp.gov.br",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Jorge Paulo Gabriel Nascimento",
                "ocupacao": "Policial Militar",
                "renda": 5000.00,
                "responsavel": True,
                "telefone": "(73) 3901-9965",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "2024-01-17",
                "escolaridade": "Créche",
                "funcao_familiar": "Filho",
                "nome": "Lucca Lucca Lima",
                "ocupacao": "Neném",
                "renda": 0.00,
                "responsavel": False,
                "beneficiario_assistencial": True,
            },
        ]
    }

    response = test_client.post(
        "/agape/cadastrar-membros/9999",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}


def test_register_agape_members_error_family_deleted(
    test_client: FlaskClient, seed_admin_user_token, seed_family_deleted
):
    familia = seed_family_deleted
    payload = {
        "membros": [
            {
                "data_nascimento": "2001-01-07",
                "email": "jorge_nascimento@policiamilitar.sp.gov.br",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Jorge Paulo Gabriel Nascimento",
                "ocupacao": "Policial Militar",
                "renda": 5000.00,
                "responsavel": True,
                "telefone": "(73) 3901-9965",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "2024-01-17",
                "escolaridade": "Créche",
                "funcao_familiar": "Filho",
                "nome": "Lucca Lucca Lima",
                "ocupacao": "Neném",
                "renda": 0.00,
                "responsavel": False,
                "beneficiario_assistencial": True,
            },
        ]
    }

    response = test_client.post(
        f"/agape/cadastrar-membros/{familia.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}


def test_register_agape_members_error_cpf_already_exists(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_family_with_members,
):
    familia, membros = seed_agape_family_with_members

    payload = {
        "membros": [
            {
                "data_nascimento": "2001-01-07",
                "email": "jorge_nascimento@policiamilitar.sp.gov.br",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Jorge Paulo Gabriel Nascimento",
                "ocupacao": "Policial Militar",
                "renda": 5000.00,
                "responsavel": True,
                "telefone": "(73) 3901-9965",
                "cpf": membros[0].cpf,
                "beneficiario_assistencial": True,
            },
        ]
    }

    response = test_client.post(
        f"/agape/cadastrar-membros/{familia.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Ja existe um membro com o CPF {membros[0].cpf} cadastrado."
    }


def test_register_agape_members_error_email_already_exists(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_family_with_members,
):
    familia, membros = seed_agape_family_with_members

    payload = {
        "membros": [
            {
                "data_nascimento": "2001-01-07",
                "email": membros[0].email,
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Jorge Paulo Gabriel Nascimento",
                "ocupacao": "Policial Militar",
                "renda": 5000.00,
                "telefone": "(73) 3901-9965",
                "beneficiario_assistencial": True,
            },
        ]
    }

    response = test_client.post(
        f"/agape/cadastrar-membros/{familia.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Já existe um membro com o email {membros[0].email} cadastrado."
    }
