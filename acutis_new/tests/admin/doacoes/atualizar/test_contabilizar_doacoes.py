from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.doacao import Doacao
from acutis_api.infrastructure.extensions import database


def test_contabilizar_doacao_nao_encontrada(client: FlaskClient, membro_token):
    id_nao_existente = '5CEC4AE4-3FDC-4A96-BDDD-15931A5161AB'

    response = client.put(
        f'/api/admin/doacoes/contabilizar-doacao/{id_nao_existente}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Doação não encontrada'}]


def test_contabilizar_doacao_sucessso(
    client: FlaskClient, membro_token, seed_dados_doacao, seed_campanha_doacao
):
    _, doacao = seed_dados_doacao(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.put(
        f'/api/admin/doacoes/contabilizar-doacao/{doacao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'msg': 'Doação descontabilizada com sucesso.'
    }
    verificar_doacao = (
        database.session.query(Doacao).filter(Doacao.id == doacao.id).first()
    )

    assert verificar_doacao.contabilizar == False
