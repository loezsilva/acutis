from http import HTTPStatus
from flask.testing import FlaskClient
from datetime import datetime


def test_stats_by_geolocation_sendgrid_success(
    test_client: FlaskClient,
    seed_admin_user_token,
):
    
    initial_date = datetime.now().strftime("%Y-%m-%d")
    final_date = datetime.now().strftime("%Y-%m-%d")
        
    response = test_client.get(
        f"/mensageria/estatisticas-por-geolocalizacao?initial_date={initial_date}&final_date={final_date}&aggregated_by=day",
        headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    
def test_stats_by_geolocation_sendgrid_unauthorized(
    test_client: FlaskClient,
):
    
    initial_date = datetime.now().strftime("%Y-%m-%d")
    final_date = datetime.now().strftime("%Y-%m-%d")
        
    response = test_client.get(
        f"/mensageria/estatisticas-por-geolocalizacao?initial_date={initial_date}&final_date={final_date}&aggregated_by=day",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED