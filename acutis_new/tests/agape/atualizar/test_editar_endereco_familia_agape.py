import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

EDITAR_ENDERECO_FAMILIA_ENDPOINT = 'api/agape/editar-endereco-familia'


def test_editar_endereco_familia_sucesso(
    client: FlaskClient,
    seed_familia_com_endereco,
    membro_token,
):
    """Testa a edição bem-sucedida do endereço de uma família ágape."""
    familia = seed_familia_com_endereco[0]

    dados_edicao = {
        'cep': '12345000',
        'rua': 'Rua Nova Teste',
        'numero': '100A',
        'complemento': 'Casa Nova',
        'ponto_referencia': 'Perto da Praça Nova',
        'bairro': 'Bairro Novo',
        'cidade': 'Cidade Nova',
        'estado': 'SP',
    }

    resposta = client.put(
        f'{EDITAR_ENDERECO_FAMILIA_ENDPOINT}/{familia.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.OK


def test_editar_endereco_familia_dados_invalidos_campos_obrigatorios_faltando(
    client: FlaskClient, seed_familia_com_endereco, membro_token
):
    """
    Testa a edição do endereço de uma família com campos obrigatórios faltando.
    """
    familia, _ = seed_familia_com_endereco

    dados_edicao_invalidos = {
        'cep': '12345000',
        'numero': '100A',
        'bairro': 'Bairro Novo',
        'cidade': 'Cidade Nova',
        'estado': 'SP',
    }

    resposta = client.put(
        f'{EDITAR_ENDERECO_FAMILIA_ENDPOINT}/{familia.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_edicao_invalidos,
    )

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_editar_endereco_familia_dados_invalidos_cep_formato_incorreto(
    client: FlaskClient,
    seed_familia_com_endereco,
    seed_lead_voluntario_e_token,
):
    """
    Testa a edição do endereço de uma família com CEP em formato incorreto.
    """
    familia, _ = seed_familia_com_endereco
    _, token = seed_lead_voluntario_e_token

    dados_edicao_invalidos = {
        'cep': '12345-000A',
        'rua': 'Rua Valida',
        'numero': '100',
        'bairro': 'Bairro Valido',
        'cidade': 'Cidade Valida',
        'estado': 'CE',
    }

    resposta = client.put(
        f'{EDITAR_ENDERECO_FAMILIA_ENDPOINT}/{familia.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=dados_edicao_invalidos,
    )

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) > 0
    assert any(detalhe['loc'] == ['cep'] for detalhe in resposta_json)


def test_editar_endereco_familia_dados_invalidos_estado_formato_incorreto(
    client: FlaskClient,
    seed_familia_com_endereco,
    membro_token,
):
    """
    Testa a edição do endereço de uma família com estado em formato incorreto.
    """
    familia, _ = seed_familia_com_endereco

    dados_edicao_invalidos = {
        'cep': '60000000',
        'rua': 'Rua Valida',
        'numero': '100',
        'bairro': 'Bairro Valido',
        'cidade': 'Cidade Valida',
        'estado': 'CEARA',  # Formato incorreto, deve ser UF com 2 chars
    }

    resposta = client.put(
        f'{EDITAR_ENDERECO_FAMILIA_ENDPOINT}/{familia.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_edicao_invalidos,
    )

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) > 0
    assert any(
        detalhe['loc'] == ['estado']
        and 'String should have at most 2 characters' in detalhe['msg']
        for detalhe in resposta_json
    )


def test_editar_endereco_familia_nao_encontrada(
    client: FlaskClient, membro_token
):
    """
    Testa a tentativa de edição do endereço de uma família que não existe.
    """

    uuid_invalido = uuid.uuid4()

    dados_edicao = {
        'cep': '12345000',
        'rua': 'Rua Fantasma',
        'numero': 'SN',
        'bairro': 'Bairro Inexistente',
        'cidade': 'Cidade de Ninguém',
        'estado': 'XX',
    }

    resposta = client.put(
        f'{EDITAR_ENDERECO_FAMILIA_ENDPOINT}/{uuid_invalido}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) > 0
    assert 'msg' in resposta_json[0]
    assert 'não encontrada' in resposta_json[0]['msg']


def test_editar_endereco_familia_sem_permissao(
    client: FlaskClient, seed_familia_com_endereco
):
    """
    Testa a tentativa de edição do endereço de uma família sem permissão.
    """
    familia, _ = seed_familia_com_endereco

    dados_edicao = {
        'cep': '12345000',
        'rua': 'Rua Proibida',
        'numero': '403',
        'bairro': 'Bairro Restrito',
        'cidade': 'Cidade Fechada',
        'estado': 'ZZ',
    }

    resposta = client.put(
        f'{EDITAR_ENDERECO_FAMILIA_ENDPOINT}/{familia.id}',
        json=dados_edicao,
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
