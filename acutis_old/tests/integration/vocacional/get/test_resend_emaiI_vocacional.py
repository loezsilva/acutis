from http import HTTPStatus
from flask.testing import FlaskClient


def test_resend_email_vocacional(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_pre_cadastro_vocacional_aproved,
):

    pre_cadastro, etapa = seed_pre_cadastro_vocacional_aproved

    response = test_client.post(
        "/vocacional/reenviar-email-vocacional",
        headers=seed_admin_user_token,
        json={"usuario_vocacional_id": pre_cadastro.id},
        content_type="application/json"
    )
     
    assert response.status_code == HTTPStatus.OK


def test_resend_email_vocacional_reproved(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_pre_cadastro_vocacional_reproved,
):

    pre_cadastro, etapa = seed_pre_cadastro_vocacional_reproved

    response = test_client.post(
        "/vocacional/reenviar-email-vocacional",
        headers=seed_admin_user_token,
        json={"usuario_vocacional_id": pre_cadastro.id},
        content_type="application/json"
    )
     
    assert response.status_code == HTTPStatus.CONFLICT
    data_response = response.get_json()
    
    assert data_response["error"] == "Não foi possível enviar o email pois o processo foi marcado como reprovado ou desistente ou pendente."
    
def test_resend_email_vocacional_desistencia(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_pre_cadastro_vocacional_desistencia,
):

    pre_cadastro, etapa = seed_pre_cadastro_vocacional_desistencia

    response = test_client.post(
        "/vocacional/reenviar-email-vocacional",
        headers=seed_admin_user_token,
        json={"usuario_vocacional_id": pre_cadastro.id},
        content_type="application/json"
    )
     
    assert response.status_code == HTTPStatus.CONFLICT
    data_response = response.get_json()
    
    assert data_response["error"] == "Não foi possível enviar o email pois o processo foi marcado como reprovado ou desistente ou pendente."
    
def test_resend_email_vocacional_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
):

    response = test_client.post(
        "/vocacional/reenviar-email-vocacional",
        headers=seed_admin_user_token,
        json={"usuario_vocacional_id": 494949},
        content_type="application/json"
    )
     
    assert response.status_code == HTTPStatus.NOT_FOUND
    data_response = response.get_json()
    
    assert data_response["error"] == "Vocacional não encontrado."