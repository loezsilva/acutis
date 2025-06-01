import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BUSCAR_ITENS_ENDPOINT = (
    '/api/agape/buscar-itens-ciclo-acao-agape/{acao_agape_id}'
)


def test_buscar_itens_ciclo_acao_sucesso_com_itens(
    client: FlaskClient, membro_token, seed_ciclo_acao_com_itens
):
    ciclo_acao, itens_esperados = seed_ciclo_acao_com_itens

    response = client.get(
        BUSCAR_ITENS_ENDPOINT.format(acao_agape_id=ciclo_acao.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    resultados_esperados = response_data['resultados']

    assert isinstance(resultados_esperados, list)
    assert len(resultados_esperados) == len(itens_esperados)

    ids_dos_items_da_response = {item['id'] for item in resultados_esperados}
    ids_dos_items_esperados = {str(item.id) for item in itens_esperados}
    assert sorted(ids_dos_items_da_response) == sorted(ids_dos_items_esperados)


def test_buscar_itens_ciclo_acao_sucesso_sem_itens(
    client: FlaskClient,
    membro_token,
    seed_ciclo_acao_agape,
):
    """Testa a busca de itens de um ciclo de ação que não possui itens."""
    ciclo_acao = seed_ciclo_acao_agape[0]

    response = client.get(
        BUSCAR_ITENS_ENDPOINT.format(acao_agape_id=ciclo_acao.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json
    resultados = response_data['resultados']
    assert isinstance(resultados, list)
    assert len(resultados) == 0


def test_buscar_itens_ciclo_acao_nao_encontrado(
    client: FlaskClient, membro_token
):
    """Testa a busca de itens para um ciclo de ação inexistente."""
    id_inexistente = uuid.uuid4()

    response = client.get(
        BUSCAR_ITENS_ENDPOINT.format(acao_agape_id=id_inexistente),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
