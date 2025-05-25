from http import HTTPStatus
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from builder import db

from models.perfil import Perfil, ProfilesEnum
from models.permissao_usuario import PermissaoUsuario
from models.schemas.agape.get.get_agape_volunteers import AgapeVoluntarySchema
from tests.factories import UsuarioFactory


def test_get_agape_volunteers_success(
    test_client: FlaskClient, seed_admin_user_token
):
    perfil = Perfil.query.filter_by(nome=ProfilesEnum.VOLUNTARIO_AGAPE).first()
    usuario = UsuarioFactory()
    db.session.add(usuario)
    db.session.flush()

    permissao_usuario = PermissaoUsuario(
        fk_usuario_id=usuario.id,
        fk_perfil_id=perfil.id,
        usuario_criacao=0,
    )
    db.session.add(permissao_usuario)
    db.session.commit()

    response = test_client.get(
        "/agape/listar-voluntarios-agape", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["voluntarios"] == [
        AgapeVoluntarySchema.from_orm(usuario).dict()
    ]


def test_get_agape_volunteers_error_forbidden(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, _ = seed_user_with_dependencies
    token = create_access_token(identity=user.id)

    response = test_client.get(
        "/agape/listar-voluntarios-agape",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {
        "error": "Você não tem permissão para realizar esta ação."
    }
