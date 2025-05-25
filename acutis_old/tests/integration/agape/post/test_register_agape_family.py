from http import HTTPStatus
from io import BytesIO
import json
from faker import Faker
from flask.testing import FlaskClient
import base64

faker = Faker("pt-BR")


def test_register_agape_family_success(
    test_client: FlaskClient, seed_admin_user_token
):
    comprovante_residencia = (BytesIO(b"fake image data"), "avatar.jpg")
    fotos_familia = [
        (BytesIO(b"fake image"), "foto1.jpg"),
        (BytesIO(b"fake image 2"), "foto2.jpg"),
    ]

    foto_documento = BytesIO(b'conteudo_simulado_da_imagem')
    foto_documento_base64 = (
        "data:image/jpeg;base64," + base64.b64encode(foto_documento.getvalue()).decode("utf-8")
    )

    endereco = json.dumps(
        {
            "bairro": "Jardim Tropical",
            "cep": "65910-751",
            "cidade": "Imperatriz",
            "complemento": "Bloco 10, Apto 403",
            "estado": "MA",
            "numero": "1240",
            "ponto_referencia": "Próximo ao mercantil",
            "rua": "Rua CD-2",
        }
    )
    membros = json.dumps(
        [
            {
                "cpf": faker.cpf(),
                "data_nascimento": "1987-01-03",
                "email": faker.email(domain="gmail.com"),
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Antonio Isaac Cardoso",
                "ocupacao": "Engenheiro Mecânico",
                "renda": 10000,
                "responsavel": True,
                "telefone": "3129361259",
                "beneficiario_assistencial": False,
                "foto_documento": foto_documento_base64
            },
            {
                "cpf": faker.cpf(),
                "data_nascimento": "1964-01-04",
                "email": faker.email(domain="gmail.com"),
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Mãe",
                "nome": "Amanda Analu Monteiro",
                "ocupacao": "Engenheira Elétrica",
                "renda": 8500,
                "responsavel": True,
                "telefone": "(84) 99820-8486",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "1998-01-21",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Filho",
                "nome": "Eliel Da Vinci Barbosa",
                "ocupacao": "Engenheiro Mecatrônico",
                "renda": 15000,
                "beneficiario_assistencial": False,
            },
        ],
    )

    response = test_client.post(
        "/agape/cadastrar-familia",
        data={
            "endereco": endereco,
            "membros": membros,
            "comprovante_residencia": comprovante_residencia,
            "observacao": "Observação",
            "fotos_familia": fotos_familia,
        },
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Família cadastrada com sucesso."}


def test_register_agape_family_one_responsible(
    test_client: FlaskClient, seed_admin_user_token
):
    endereco = json.dumps(
        {
            "bairro": "Jardim Tropical",
            "cep": "65910-751",
            "cidade": "Imperatriz",
            "complemento": "Bloco 10, Apto 403",
            "estado": "MA",
            "numero": "1240",
            "ponto_referencia": "Próximo ao mercantil",
            "rua": "Rua CD-2",
        }
    )
    membros = json.dumps(
        [
            {
                "cpf": faker.cpf(),
                "data_nascimento": "1987-01-03",
                "email": faker.email(domain="gmail.com"),
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Antonio Isaac Cardoso",
                "ocupacao": "Engenheiro Mecânico",
                "renda": 10000,
                "responsavel": True,
                "telefone": "3129361259",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "1998-01-21",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Filho",
                "nome": "Eliel Da Vinci Barbosa",
                "ocupacao": "Engenheiro Mecatrônico",
                "renda": 15000,
                "beneficiario_assistencial": False,
            },
        ],
    )

    response = test_client.post(
        "/agape/cadastrar-familia",
        data={
            "endereco": endereco,
            "membros": membros,
            "observacao": "Observação",
        },
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Família cadastrada com sucesso."}


def test_register_agape_family_without_responsible(
    test_client: FlaskClient, seed_admin_user_token
):
    endereco = json.dumps(
        {
            "bairro": "Jardim Tropical",
            "cep": "65910-751",
            "cidade": "Imperatriz",
            "complemento": "Bloco 10, Apto 403",
            "estado": "MA",
            "numero": "1240",
            "ponto_referencia": "Próximo ao mercantil",
            "rua": "Rua CD-2",
        }
    )
    membros = json.dumps(
        [
            {
                "cpf": faker.cpf(),
                "data_nascimento": "1987-01-03",
                "email": faker.email(domain="gmail.com"),
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Antonio Isaac Cardoso",
                "ocupacao": "Engenheiro Mecânico",
                "renda": 10000,
                "telefone": "3129361259",
                "beneficiario_assistencial": True,
            },
            {
                "data_nascimento": "1998-01-21",
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Filho",
                "nome": "Eliel Da Vinci Barbosa",
                "ocupacao": "Engenheiro Mecatrônico",
                "renda": 15000,
                "beneficiario_assistencial": False,
            },
        ],
    )

    response = test_client.post(
        "/agape/cadastrar-familia",
        data={
            "endereco": endereco,
            "membros": membros,
            "observacao": "Observação",
        },
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Família cadastrada com sucesso."}


def test_register_agape_family_error_responsible_without_cpf(
    test_client: FlaskClient, seed_admin_user_token
):
    endereco = json.dumps(
        {
            "bairro": "Jardim Tropical",
            "cep": "65910-751",
            "cidade": "Imperatriz",
            "complemento": "Bloco 10, Apto 403",
            "estado": "MA",
            "numero": "1240",
            "ponto_referencia": "Próximo ao mercantil",
            "rua": "Rua CD-2",
        }
    )
    membros = json.dumps(
        [
            {
                "data_nascimento": "1987-01-03",
                "email": faker.email(domain="gmail.com"),
                "escolaridade": "Ensino Superior Completo",
                "funcao_familiar": "Pai",
                "nome": "Antonio Isaac Cardoso",
                "ocupacao": "Engenheiro Mecânico",
                "renda": 10000,
                "responsavel": True,
                "telefone": "3129361259",
                "beneficiario_assistencial": True,
            },
        ],
    )

    response = test_client.post(
        "/agape/cadastrar-familia",
        data={
            "endereco": endereco,
            "membros": membros,
            "observacao": "Observação",
        },
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "error": "O CPF do responsável Antonio Isaac Cardoso é obrigatório."
    }


def test_register_agape_family_error_cpf_already_exists(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_family_with_members,
):
    _, membros = seed_agape_family_with_members

    cpf = membros[0].cpf

    endereco = json.dumps(
        {
            "bairro": "Jardim Tropical",
            "cep": "65910-751",
            "cidade": "Imperatriz",
            "complemento": "Bloco 10, Apto 403",
            "estado": "MA",
            "numero": "1240",
            "ponto_referencia": "Próximo ao mercantil",
            "rua": "Rua CD-2",
        }
    )
    membros = json.dumps(
        {
            "data_nascimento": "1987-01-03",
            "email": faker.email(domain="gmail.com"),
            "escolaridade": "Ensino Superior Completo",
            "funcao_familiar": "Pai",
            "nome": "Antonio Isaac Cardoso",
            "ocupacao": "Engenheiro Mecânico",
            "renda": 10000,
            "telefone": "3129361259",
            "responsavel": True,
            "cpf": cpf,
            "beneficiario_assistencial": True,
        },
    )

    response = test_client.post(
        "/agape/cadastrar-familia",
        data={
            "endereco": endereco,
            "membros": membros,
            "observacao": "Observação",
        },
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Já existe um membro com o CPF {cpf} cadastrado."
    }


def test_register_agape_family_error_email_already_exists(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_family_with_members,
):
    _, membros = seed_agape_family_with_members
    email = membros[0].email

    endereco = json.dumps(
        {
            "bairro": "Jardim Tropical",
            "cep": "65910-751",
            "cidade": "Imperatriz",
            "complemento": "Bloco 10, Apto 403",
            "estado": "MA",
            "numero": "1240",
            "ponto_referencia": "Próximo ao mercantil",
            "rua": "Rua CD-2",
        }
    )
    membros = json.dumps(
        {
            "data_nascimento": "1987-01-03",
            "email": email,
            "escolaridade": "Ensino Superior Completo",
            "funcao_familiar": "Pai",
            "nome": "Antonio Isaac Cardoso",
            "ocupacao": "Engenheiro Mecânico",
            "renda": 10000,
            "telefone": "3129361259",
            "responsavel": True,
            "cpf": faker.cpf(),
            "beneficiario_assistencial": True,
        },
    )

    response = test_client.post(
        "/agape/cadastrar-familia",
        data={
            "endereco": endereco,
            "membros": membros,
            "observacao": "Observação",
        },
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Já existe um membro com o email {email} cadastrado."
    }
