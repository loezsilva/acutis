from http import HTTPStatus

from flask.testing import FlaskClient

LISTAR_ENDERECOS_FAMILIAS_ENDPOINT = (
    'api/agape/listar-enderecos-familias-agape'
)


def test_listar_enderecos_familias_sucesso_com_dados(
    client: FlaskClient,
    seed_diversas_familias_para_exportacao,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de endereços de múltiplas famílias ágape.
    Apenas famílias ativas devem ser listadas.
    """
    familias_ativas_esperadas = seed_diversas_familias_para_exportacao

    resposta = client.get(
        LISTAR_ENDERECOS_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    resultados = resposta_json['resultados']

    assert isinstance(resultados, list)
    assert len(resultados) == len(familias_ativas_esperadas), (
        'O número de endereços listados não corresponde ao número '
        'de famílias ativas.'
    )


def test_listar_enderecos_familias_sem_dados(
    client: FlaskClient,
    membro_token,
):
    """
    Testa a listagem de endereços de famílias quando não há famílias
    ativas cadastradas (ou nenhuma família).
    Espera-se uma lista vazia como resposta.
    """

    resposta = client.get(
        LISTAR_ENDERECOS_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json['resultados']

    assert isinstance(resposta_json, list)
    assert len(resposta_json) == 0, (
        'A lista de endereços de famílias deveria estar vazia.'
    )


def test_listar_enderecos_familias_sem_permissao(
    client: FlaskClient,
):
    resposta = client.get(
        LISTAR_ENDERECOS_FAMILIAS_ENDPOINT,
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
