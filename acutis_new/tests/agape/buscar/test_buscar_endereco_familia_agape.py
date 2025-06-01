import uuid
from http import HTTPStatus

BUSCAR_ENDERECO_FAMILIA_ENDPOINT = '/api/agape/buscar-endereco-familia'


def test_buscar_endereco_familia_sucesso(
    client, seed_familia_com_endereco, membro_token
):
    familia_criada, endereco_esperado = seed_familia_com_endereco

    response = client.get(
        f'{BUSCAR_ENDERECO_FAMILIA_ENDPOINT}/{familia_criada.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    dados_resposta = response.json

    assert dados_resposta['id'] == str(endereco_esperado.id)
    assert dados_resposta['logradouro'] == endereco_esperado.logradouro
    assert dados_resposta['numero'] == endereco_esperado.numero
    assert dados_resposta['bairro'] == endereco_esperado.bairro
    assert dados_resposta['cidade'] == endereco_esperado.cidade
    assert dados_resposta['estado'] == endereco_esperado.estado
    assert dados_resposta['codigo_postal'] == endereco_esperado.codigo_postal
    if endereco_esperado.complemento:
        assert dados_resposta['complemento'] == endereco_esperado.complemento
    else:
        assert dados_resposta.get('complemento') is None

    assert 'nome_familia' not in dados_resposta


def test_buscar_endereco_familia_nao_encontrada(
    client,
    membro_token,
):
    familia_id_invalida = uuid.uuid4()

    response = client.get(
        f'{BUSCAR_ENDERECO_FAMILIA_ENDPOINT}/{familia_id_invalida}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_buscar_endereco_familia_sem_autenticacao(
    client, seed_familia_com_endereco
):
    familia_criada, _ = seed_familia_com_endereco

    response = client.get(
        f'{BUSCAR_ENDERECO_FAMILIA_ENDPOINT}/{familia_criada.id}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
