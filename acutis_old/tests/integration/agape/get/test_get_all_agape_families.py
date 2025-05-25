from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_agape_families_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_families_infos
):
    familia = seed_agape_families_infos
    qtd_membros = 10
    qtd_recebimentos = 5

    response = test_client.get(
        "/agape/listar-familias", headers=seed_admin_user_token
    )
    assert response.status_code == HTTPStatus.OK
    familias = response.json["familias"]
    for f in familias:
        if f["id"] == familia.id:
            assert f["familia"] == familia.nome_familia
            assert f["membros"] == qtd_membros
            assert f["recebimentos"] == qtd_recebimentos
