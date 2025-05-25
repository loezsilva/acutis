import pytest
from builder import db
from http import HTTPStatus
from flask.testing import FlaskClient
from models.pedido import Pedido

@pytest.mark.skip(reason='corrigir teste, nao esta funcionando')
def test_cancelar_doacao_recorrente_success(test_client: FlaskClient, seed_pedido_recorrente, seed_admin_user_token):
    pedido, processamento_pedido = seed_pedido_recorrente
    
    response = test_client.post(
        f"/checkout/payment/cancel-recurrence/{pedido.id}",
        headers=seed_admin_user_token
    )    
    
    assert response.status_code == HTTPStatus.OK
    
    verificar_cancelamento = db.session.query(Pedido).filter(Pedido.id == pedido.id).first()
    
    assert verificar_cancelamento != None
    assert verificar_cancelamento.cancelada_em != None
    assert verificar_cancelamento.cancelada_por != None

def test_cancelar_doacao_recorrente_nao_autorizado(test_client: FlaskClient, seed_pedido_recorrente):
    pedido, processamento_pedido = seed_pedido_recorrente
    
    response = test_client.post(
        f"/checkout/payment/cancel-recurrence/{pedido.id}",
    )    

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    