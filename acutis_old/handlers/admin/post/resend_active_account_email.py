from typing import Tuple

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.usuario import Usuario
from templates.email_templates import active_account_email_template
from utils.send_email import send_email
from utils.token_email import generate_token


class ResendActiveAccountEmail:
    def execute(self, fk_usuario_id: int) -> Tuple:
        user = self.__get_user_data(fk_usuario_id)
        self.__resend_active_account_email(user)

        return {"msg": "Email enviado com sucesso!"}, 200

    def __get_user_data(self, fk_usuario_id: int) -> Usuario:
        user: Usuario = Usuario.query.filter_by(
            id=fk_usuario_id, deleted_at=None
        ).first()
        if user is None:
            raise NotFoundError("Usuário não encontrado.")

        if user.status:
            raise ConflictError("Usuário já está ativo.")

        return user

    def __resend_active_account_email(self, user: Usuario) -> None:
        payload = {"email": user.email}
        token = generate_token(obj=payload, salt="active_account_confirmation")
        html = active_account_email_template(user.nome, token)
        send_email("HeSed - Verificação de Email", user.email, html, 1)
