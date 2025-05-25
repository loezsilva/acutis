from http import HTTPStatus
import io
from flask.testing import FlaskClient


def test_register_agape_donation_receipts_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_donation
):
    doacao_agape = seed_agape_donation

    recibo = (io.BytesIO(b"fake_image_data"), "recibo.jpg")

    payload = {"recibos": [recibo, recibo]}

    response = test_client.post(
        f"/agape/registrar-recibos-doacao-agape/{doacao_agape.id}",
        headers=seed_admin_user_token,
        data=payload,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        "msg": "Recibos da doação registrados com sucesso."
    }


def test_register_agape_donation_receipts_error_file_name(
    test_client: FlaskClient, seed_admin_user_token
):
    recibo = (io.BytesIO(b"fake_image_data"), "")

    payload = {"recibos": [recibo, recibo]}

    response = test_client.post(
        f"/agape/registrar-recibos-doacao-agape/9999",
        headers=seed_admin_user_token,
        data=payload,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"error": "Nome do arquivo inválido."}


def test_register_agape_donation_receipts_error_file_extension(
    test_client: FlaskClient, seed_admin_user_token
):
    recibo = (io.BytesIO(b"fake_image_data"), "recibo.gif")

    payload = {"recibos": [recibo, recibo]}

    response = test_client.post(
        f"/agape/registrar-recibos-doacao-agape/9999",
        headers=seed_admin_user_token,
        data=payload,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"error": "Extensão do arquivo não permitida."}


def test_register_agape_donation_receipts_error_donation_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    recibo = (io.BytesIO(b"fake_image_data"), "recibo.jpg")

    payload = {"recibos": [recibo, recibo]}

    response = test_client.post(
        f"/agape/registrar-recibos-doacao-agape/9999",
        headers=seed_admin_user_token,
        data=payload,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Doação ágape não encontrada."}
