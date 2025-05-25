from http import HTTPStatus
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from models.perfil import Perfil, ProfilesEnum
from models.permissao_usuario import PermissaoUsuario
from tests.factories import UsuarioFactory
from builder import db


def test_remove_user_from_agape_voluntary_success(
    test_client: FlaskClient, seed_admin_user_token
):
    perfil_benfeitor = Perfil.query.filter_by(
        nome=ProfilesEnum.BENFEITOR
    ).first()
    perfil_voluntario = Perfil.query.filter_by(
        nome=ProfilesEnum.VOLUNTARIO_AGAPE
    ).first()
    usuario = UsuarioFactory()
    db.session.add(usuario)
    db.session.flush()

    permissao_usuario = PermissaoUsuario(
        fk_usuario_id=usuario.id,
        fk_perfil_id=perfil_voluntario.id,
        usuario_criacao=0,
    )
    db.session.add(permissao_usuario)
    db.session.commit()

    response = test_client.delete(
        f"/agape/remover-voluntario-agape/{usuario.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    db.session.refresh(permissao_usuario)
    assert permissao_usuario.fk_perfil_id == perfil_benfeitor.id


def test_remove_user_from_agape_voluntary_error_forbidden(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, _ = seed_user_with_dependencies
    token = create_access_token(identity=user.id)

    response = test_client.delete(
        f"/agape/remover-voluntario-agape/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {
        "error": "Você não tem permissão para realizar esta ação."
    }
