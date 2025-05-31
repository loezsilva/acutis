from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.infrastructure.extensions import database
from tests.factories import EnderecoFactory, LeadFactory, MembroFactory


def test_listar_doacoes_sucesso(
    client: FlaskClient, seed_campanha_doacao, seed_dados_doacao
):
    quantidade_registros = 1

    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(campanha=campanha)

    payload = {'email': lead.email, 'senha': '@Teste;1234'}  # NOSONAR

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.get(
        '/api/membros/listar-doacoes',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == quantidade_registros
    assert response.json['doacoes'][0]['doacao_id'] == str(doacao.id)
    assert response.json['doacoes'][0]['nome_campanha'] == campanha.nome


def test_listar_doacoes_erro_membro_sem_benfeitor(
    client: FlaskClient,
):
    endereco = EnderecoFactory()
    database.session.add(endereco)
    lead = LeadFactory()
    lead.senha = '@Teste;1234'
    lead.status = True
    database.session.add(lead)
    membro = MembroFactory(fk_lead_id=lead.id, fk_endereco_id=endereco.id)
    database.session.add(membro)
    database.session.commit()

    payload = {'email': lead.email, 'senha': '@Teste;1234'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.get(
        '/api/membros/listar-doacoes',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Nenhuma doação encontrada.'}]
