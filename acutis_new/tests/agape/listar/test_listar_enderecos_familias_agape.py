import uuid
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

    assert isinstance(resposta_json, list)
    assert len(resposta_json) == len(familias_ativas_esperadas), (
        'O número de endereços listados não corresponde ao número '
        'de famílias ativas.'
    )

    enderecos_resposta_por_familia_id = {
        uuid.UUID(item['familia_id']): item for item in resposta_json
    }

    for familia_esperada in familias_ativas_esperadas:
        assert familia_esperada.id in enderecos_resposta_por_familia_id, (
            f'Família ID {familia_esperada.id} esperada mas não '
            f'encontrada na resposta.'
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
    resposta_json = resposta.json

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
