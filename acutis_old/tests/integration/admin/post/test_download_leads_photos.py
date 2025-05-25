from flask.testing import FlaskClient

from builder import db


def test_download_leads_photos_success(
    test_client: FlaskClient, seed_admin_user_token, seed_foto_leads
):
    lead_1, lead_2, foto_1, foto_2 = seed_foto_leads

    payload = {"ids_leads": [lead_1.id, lead_2.id]}

    response = test_client.post(
        "/administradores/baixar-fotos-leads",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Fotos de leads baixadas com sucesso!"

    db.session.refresh(foto_1)
    db.session.refresh(foto_2)
    assert foto_1.user_download is not None
    assert foto_2.user_download is not None
    assert foto_1.data_download is not None
    assert foto_2.data_download is not None
