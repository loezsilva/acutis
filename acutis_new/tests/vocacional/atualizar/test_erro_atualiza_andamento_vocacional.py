from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.infrastructure.extensions import database
from tests.factories import LeadFactory, UsuarioVocacionalFactory


def test_usuario_invalido_atualiza_andamento_vocacional(
    client: FlaskClient,
    seed_pre_cadastro_vocacional_pendentes,
    membro_token,
):
    # TODO usar o user admin, quando desenvolvido

    lead = LeadFactory()

    response = client.put(
        '/api/vocacional/atualizar-andamento-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'acao': 'aprovar', 'usuario_vocacional_id': lead.id},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    message = response.get_json()
    assert message == [{'msg': 'Usuário não encontrado'}]


def test_etapa_invalida_atualiza_andamento_vocacional(
    client: FlaskClient,
    membro_token,
):
    # TODO usar o user admin, quando desenvolvido

    usuario = UsuarioVocacionalFactory()
    database.session.add(usuario)
    database.session.commit()

    response = client.put(
        '/api/vocacional/atualizar-andamento-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'acao': 'aprovar', 'usuario_vocacional_id': usuario.id},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    message = response.get_json()
    assert message == [{'msg': 'Nenhuma etapa encontrada'}]
