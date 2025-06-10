import uuid
from http import HTTPStatus
from io import BytesIO

from flask.testing import FlaskClient

EDITAR_MEMBRO_AGAPE_ENDPOINT = 'api/agape/editar-membro'


def test_editar_membro_agape_sucesso(
    client: FlaskClient,
    seed_membro_agape,
    seed_lead_voluntario_e_token,
):
    membro_existente = seed_membro_agape
    _, token = seed_lead_voluntario_e_token

    dados_edicao = {
        'cpf': '051.183.070-07',
        'responsavel': True,
        'data_nascimento': '1990-01-01',
        'nome': 'Nome Atualizado do Membro',
        'telefone': '999887766',
        'renda': 1500.75,
        'escolaridade': 'Superior Incompleto',
        'funcao_familiar': 'filho',
        'beneficiario_assistencial': False,
        'ocupacao': 'Ocupação de teste',
        'foto_documento': (BytesIO(b'foto'), 'foto_teste.png'),
    }

    resposta = client.put(
        f'{EDITAR_MEMBRO_AGAPE_ENDPOINT}/{membro_existente.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    assert (
        resposta_json['msg'].lower()
        == 'Membro ágape atualizado com sucesso.'.lower()
    )


def test_editar_membro_agape_email_invalido(
    client: FlaskClient,
    seed_membro_agape,
    membro_token,
):
    """Testa a edição de um membro ágape com email inválido."""
    membro_existente = seed_membro_agape

    dados_edicao = {'email': 'email_invalido_sem_arroba.com'}

    resposta = client.put(
        f'{EDITAR_MEMBRO_AGAPE_ENDPOINT}/{membro_existente.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) > 0
    assert any(
        (
            detalhe['loc'] == ['email']
            and 'value is not a valid email address' in detalhe['msg']
        )
        for detalhe in resposta_json
    )


def test_editar_membro_agape_cpf_formato_invalido(
    client: FlaskClient,
    seed_membro_agape,
    seed_lead_voluntario_e_token,
):
    """
    Testa a edição de um membro ágape com CPF em formato inválido.
    """
    membro_existente = seed_membro_agape
    _, token = seed_lead_voluntario_e_token

    dados_edicao = {'cpf': '12345678900'}  # Sem a formatação esperada

    resposta = client.put(
        f'{EDITAR_MEMBRO_AGAPE_ENDPOINT}/{membro_existente.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) > 0
    assert any(
        (
            detalhe['loc'] == ['cpf']
            and 'String should match pattern' in detalhe['msg']
        )
        for detalhe in resposta_json
    )


def test_editar_membro_agape_renda_negativa(
    client: FlaskClient,
    seed_membro_agape,
    seed_lead_voluntario_e_token,
):
    """Testa a edição de um membro ágape com renda negativa."""
    membro_existente = seed_membro_agape
    _, token = seed_lead_voluntario_e_token

    dados_edicao = {'renda': -100.00}

    resposta = client.put(
        f'{EDITAR_MEMBRO_AGAPE_ENDPOINT}/{membro_existente.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) > 0
    assert any(
        (
            detalhe['loc'] == ['renda']
            and 'Input should be greater than or equal to 0' in detalhe['msg']
        )
        for detalhe in resposta_json
    )


def test_editar_membro_agape_nao_encontrado(client: FlaskClient, membro_token):
    """
    Testa a tentativa de edição de um membro ágape que não existe.
    """
    uuid_invalido = uuid.uuid4()

    dados_edicao = {
        'cpf': '051.183.070-07',
        'responsavel': True,
        'data_nascimento': '1990-01-01',
        'nome': 'Nome Atualizado do Membro',
        'telefone': '999887766',
        'renda': 1500.75,
        'escolaridade': 'Superior Incompleto',
        'funcao_familiar': 'filho',
        'beneficiario_assistencial': False,
        'ocupacao': 'Ocupação de teste',
        'foto_documento': (BytesIO(b'foto'), 'foto_teste.png'),
    }

    resposta = client.put(
        f'{EDITAR_MEMBRO_AGAPE_ENDPOINT}/{uuid_invalido}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_editar_membro_agape_sem_permissao(
    client: FlaskClient, seed_membro_agape
):
    """
    Testa a tentativa de edição de um membro ágape sem permissão adequada.
    """
    membro_existente = seed_membro_agape

    dados_edicao = {
        'nome': 'Nome Proibido',
        'telefone': '123123123',
    }

    resposta = client.put(
        f'{EDITAR_MEMBRO_AGAPE_ENDPOINT}/{membro_existente.id}',
        data=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
