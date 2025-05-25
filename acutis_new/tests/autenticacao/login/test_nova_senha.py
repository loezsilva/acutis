from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.infrastructure.extensions import database


def test_nova_senha_sucesso(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro(status=True)[0]

    payload = {'nova_senha': '@NovaSenha456'}
    token = gerar_token(
        {'email': lead.email}, salt=TokenSaltEnum.recuperar_senha
    )
    response = client.post(
        f'/api/autenticacao/nova-senha?token={token}', json=payload
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Senha alterada com sucesso.'}

    database.session.refresh(lead)
    assert lead.verificar_senha('@NovaSenha456') is True


def test_nova_senha_usuario_inativo(
    client: FlaskClient, seed_registrar_membro
):
    lead = seed_registrar_membro()[0]

    payload = {'nova_senha': '@NovaSenha456'}

    token = gerar_token(
        {'email': lead.email}, salt=TokenSaltEnum.recuperar_senha
    )

    response = client.post(
        f'/api/autenticacao/nova-senha?token={token}', json=payload
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Senha alterada com sucesso.'}

    database.session.refresh(lead)
    assert lead.verificar_senha('@NovaSenha456') is True


def test_nova_senha_usuario_inexistente(client: FlaskClient):
    payload = {'nova_senha': '@NovaSenha456'}

    token = gerar_token(
        {'email': 'inexistente@gmail.com'}, salt=TokenSaltEnum.recuperar_senha
    )

    response = client.post(
        f'/api/autenticacao/nova-senha?token={token}', json=payload
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Usuário não encontrado'}]
