from http import HTTPStatus
from flask.testing import FlaskClient


def test_aprova_vocacional_para_proxima_etapa(
    test_client: FlaskClient,
    seed_pre_cadastro_vocacional_pendentes,
    seed_admin_user_token,
):

    registro = seed_pre_cadastro_vocacional_pendentes[0][0]

    response = test_client.put(
        "/vocacional/atualizar-andamento-vocacional",
        headers=seed_admin_user_token,
        json={"acao": "aprovar", "usuario_vocacional_id": registro.id},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()

    assert data["msg"] == "Vocacional aprovado com sucesso."
    
    
def test_conflito_ao_aprovar_vocacional(
    test_client: FlaskClient,
    seed_pre_cadastro_vocacional_reproved,
    seed_admin_user_token,
):

    registro, etapa = seed_pre_cadastro_vocacional_reproved
    
    response_conflict = test_client.put(
        "/vocacional/atualizar-andamento-vocacional",
        headers=seed_admin_user_token,
        json={"acao": "aprovar", "usuario_vocacional_id": registro.id},
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Usuário já aprovado, reprovado ou desistiu."
