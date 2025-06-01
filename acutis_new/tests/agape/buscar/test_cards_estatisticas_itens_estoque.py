from http import HTTPStatus

from flask.testing import FlaskClient

CARDS_ESTATISTICAS_ITENS_ESTOQUE_ENDPOINT = (
    '/api/agape/cards-estatisticas-itens-estoque'
)


def test_cards_estatisticas_itens_estoque_com_dados(
    client: FlaskClient,
    membro_token,
    seed_varios_itens_estoque_para_estatisticas,
):
    """
    Testa as estatísticas de itens em estoque quando há dados no sistema.
    """
    expected_stats = seed_varios_itens_estoque_para_estatisticas

    response = client.get(
        CARDS_ESTATISTICAS_ITENS_ESTOQUE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert 'itens_em_estoque' in response_data
    assert (
        int(response_data['itens_em_estoque'].split(' ')[0])
        == 
        int(expected_stats['quantidade_total_itens'])
    )


def test_cards_estatisticas_itens_estoque_sem_dados(
    client: FlaskClient, membro_token
):
    """
    Testa as estatísticas de itens em estoque quando não há itens cadastrados.
    """
    response = client.get(
        CARDS_ESTATISTICAS_ITENS_ESTOQUE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert 'itens_em_estoque' in response_data
    assert (
        int(response_data['itens_em_estoque'].split(' ')[0])
        == 
        0
    )
