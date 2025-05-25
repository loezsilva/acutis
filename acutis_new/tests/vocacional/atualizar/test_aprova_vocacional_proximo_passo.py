from http import HTTPStatus

from flask.testing import FlaskClient


def test_aprova_vocacional_para_proxima_etapa(
    client: FlaskClient,
    seed_pre_cadastro_vocacional_pendentes,
    membro_token,
):
    # TODO usar o user admin, quando desenvolvido

    registro = seed_pre_cadastro_vocacional_pendentes[0][0]

    response = client.put(
        '/api/vocacional/atualizar-andamento-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'acao': 'aprovar', 'usuario_vocacional_id': registro.id},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == {'msg': 'Vocacional aprovado com sucesso.'}


def test_conflito_ao_aprovar_vocacional(
    client: FlaskClient,
    seed_pre_cadastro_vocacional_reprovado,
    membro_token,
):
    registro, etapa = seed_pre_cadastro_vocacional_reprovado

    response_conflict = client.put(
        '/api/vocacional/atualizar-andamento-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'acao': 'aprovar', 'usuario_vocacional_id': registro.id},
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    assert response_conflict.get_json() == [
        {'msg': 'Usuário já aprovado, reprovado ou desistiu.'}
    ]
