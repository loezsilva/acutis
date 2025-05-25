from http import HTTPStatus

from flask.testing import FlaskClient


def test_reprova_vocacional(
    client: FlaskClient,
    seed_pre_cadastro_vocacional_pendentes,
    membro_token,
):
    registro = seed_pre_cadastro_vocacional_pendentes[0][0]

    vocacional_id = registro.id

    response = client.put(
        '/api/vocacional/atualizar-andamento-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'acao': 'reprovar', 'usuario_vocacional_id': vocacional_id},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'msg': 'Vocacional reprovado com sucesso.'}


def test_reprova_vocacional_conflito(
    client: FlaskClient,
    seed_pre_cadastro_vocacional_reprovado,
    membro_token,
):
    registro, _ = seed_pre_cadastro_vocacional_reprovado

    vocacional_id = registro.id

    response_conflict = client.put(
        '/api/vocacional/atualizar-andamento-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'acao': 'reprovar', 'usuario_vocacional_id': vocacional_id},
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    assert response_conflict.get_json() == [
        {
            'msg': 'Usuário já aprovado, reprovado ou desistiu.',
        },
    ]
