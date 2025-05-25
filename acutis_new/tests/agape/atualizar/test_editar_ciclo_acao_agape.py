import uuid
from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

faker = Faker(locale='pt-BR')


def json_padrao(
    seed_ciclo_acao_agape_id=uuid.uuid4(),
    seed_item_estoque_agape_id=uuid.uuid4(),
):
    return {
        'abrangencia': 'cep',
        'doacoes': [
            {'item_id': str(seed_item_estoque_agape_id), 'quantidade': 1}
        ],
        'endereco': {
            'cep': '58000000',
            'bairro': 'Bairro de teste',
            'cidade': 'Cidade de teste',
            'estado': 'RN',
            'rua': 'Rua de teste',
        },
        'nome_acao_id': str(seed_ciclo_acao_agape_id),
    }


def test_editar_ciclo_acao_sucesso(
    client: FlaskClient,
    seed_ciclo_acao_agape,
    seed_item_estoque_agape,
    membro_token,
):
    dados_json = json_padrao(
        seed_ciclo_acao_agape.fk_acao_agape_id, seed_item_estoque_agape.id
    )

    response = client.put(
        f'/api/agape/editar-ciclo-acao/{seed_ciclo_acao_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_json,
    )

    assert response.status_code == HTTPStatus.OK
    assert (
        response.json['msg'].lower() == 'ciclo da ação atualizado com sucesso.'
    )


def test_erro_editar_ciclo_acao_nome_acao_inexistente(
    client: FlaskClient,
    seed_ciclo_acao_agape,
    seed_item_estoque_agape,
    membro_token,
):
    dados_json = json_padrao(
        seed_item_estoque_agape_id=seed_item_estoque_agape.id
    )
    dados_json['nome_acao_id'] = uuid.uuid4()

    response = client.put(
        f'/api/agape/editar-ciclo-acao/{seed_ciclo_acao_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_json,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'msg' in response.json[0]


def test_erro_editar_ciclo_acao_cep_invalido(
    client: FlaskClient,
    seed_ciclo_acao_agape,
    seed_item_estoque_agape,
    membro_token,
):
    dados_json = json_padrao(
        seed_ciclo_acao_agape.fk_acao_agape_id, seed_item_estoque_agape.id
    )
    dados_json['endereco']['cep'] = '58000-000'

    response = client.put(
        f'/api/agape/editar-ciclo-acao/{seed_ciclo_acao_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_json,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    dados_resposta = response.json[0]
    assert dados_resposta['loc'][0] == 'endereco'


def test_erro_editar_ciclo_acao_abrencencia_invalida(
    client: FlaskClient,
    seed_ciclo_acao_agape,
    seed_item_estoque_agape,
    membro_token,
):
    dados_json = json_padrao(
        seed_ciclo_acao_agape.fk_acao_agape_id, seed_item_estoque_agape.id
    )
    dados_json['abrangencia'] = 'desconhecida'

    response = client.put(
        f'/api/agape/editar-ciclo-acao/{seed_ciclo_acao_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_json,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    dados_resposta = response.json[0]
    assert dados_resposta['loc'][0] == 'abrangencia'


def test_erro_editar_ciclo_acao_item_inexistente(
    client: FlaskClient, seed_ciclo_acao_agape, membro_token
):
    dados_json = json_padrao(
        seed_ciclo_acao_agape_id=seed_ciclo_acao_agape.fk_acao_agape_id
    )

    response = client.put(
        f'/api/agape/editar-ciclo-acao/{seed_ciclo_acao_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_json,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'msg' in response.json[0]
