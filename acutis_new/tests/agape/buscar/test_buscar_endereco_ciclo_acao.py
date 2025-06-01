import uuid
from http import HTTPStatus

BUSCAR_ENDERECO_CICLO_ACAO_ENDPOINT = '/api/agape/buscar-endereco-ciclo-acao'


def test_buscar_endereco_ciclo_acao_sucesso(
    client, seed_ciclo_acao_agape_com_endereco, membro_token
):
    ciclo_acao, endereco = seed_ciclo_acao_agape_com_endereco

    response = client.get(
        f'{BUSCAR_ENDERECO_CICLO_ACAO_ENDPOINT}/{ciclo_acao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    dados_resposta = response.json

    assert dados_resposta['id'] == str(endereco.id)
    assert dados_resposta['logradouro'] == endereco.logradouro
    assert dados_resposta['numero'] == endereco.numero
    assert dados_resposta['bairro'] == endereco.bairro
    assert dados_resposta['cidade'] == endereco.cidade
    assert dados_resposta['estado'] == endereco.estado
    assert dados_resposta['codigo_postal'] == endereco.codigo_postal
    if endereco.complemento:
        assert dados_resposta['complemento'] == endereco.complemento
    else:
        assert dados_resposta.get('complemento') is None

    assert 'nome_familia' not in dados_resposta


def test_buscar_endereco_ciclo_acao_nao_encontrado(
    client,
    membro_token,
):
    ciclo_acao_invalido = uuid.uuid4()

    response = client.get(
        f'{BUSCAR_ENDERECO_CICLO_ACAO_ENDPOINT}/{ciclo_acao_invalido}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_buscar_endereco_familia_sem_autenticacao(
    client,
):
    ciclo_acao_invalido = uuid.uuid4()

    response = client.get(
        f'{BUSCAR_ENDERECO_CICLO_ACAO_ENDPOINT}/{ciclo_acao_invalido}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
