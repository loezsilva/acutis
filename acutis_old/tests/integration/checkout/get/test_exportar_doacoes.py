from http import HTTPStatus
from flask.testing import FlaskClient
import pytest

def test_exportar_doacoes_success(test_client: FlaskClient, seed_admin_user_token):
    response = test_client.get(
        "/checkout/exportar-doacoes?status=0&data_inicial=2025-02-01T00:00:00&data_final=2025-02-24T23:59:59&page=1",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    
    
def test_exportar_doacoes_nao_autorizado(test_client: FlaskClient):
    response = test_client.get(
        "/checkout/exportar-doacoes?status=0&data_inicial=2025-02-01T00:00:00&data_final=2025-02-24T23:59:59&page=1"
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    
def test_exportar_recorrencias_canceladas(test_client: FlaskClient, seed_admin_user_token):
    response = test_client.get(
        "/checkout/export-donations-canceladas",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    
def test_exportar_recorrencias_canceladas_nao_autorizado(test_client: FlaskClient):
    response = test_client.get(
        "/checkout/export-donations-canceladas",
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED  
    
      
def test_exportar_recorrencias_efetuadas(test_client: FlaskClient, seed_admin_user_token):
    response = test_client.get(
        "/checkout/export-recurrences-made",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    
def test_exportar_recorrencias_efetuadas_nao_autorizado(test_client: FlaskClient):
    response = test_client.get(
        "/checkout/export-recurrences-made",
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED    

@pytest.mark.skip(reason="Essa rota realiza consulta cuja não e suportada pelo sqlite") 
def test_exportar_recorrencias_previstas(test_client: FlaskClient, seed_admin_user_token):
    response = test_client.get(
        "/checkout/export-recurrences-planned",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK

def test_exportar_recorrencias_previstas_nao_autorizado(test_client: FlaskClient):
    response = test_client.get(
        "/checkout/export-recurrences-planned",
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED    
    
@pytest.mark.skip(reason="Essa rota realiza consulta cuja não e suportada pelo sqlite")
def test_exportar_recorrencias_em_lapso(test_client: FlaskClient, seed_admin_user_token):
    response = test_client.get(
        "/checkout/export-recurrences-not-paid",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    
    
def test_exportar_recorrencias_em_lapso_nao_autorizado(test_client: FlaskClient):
    response = test_client.get(
        "/checkout/export-recurrences-not-paid",
    )
    
    assert response.status_code == HTTPStatus.UNAUTHORIZED   