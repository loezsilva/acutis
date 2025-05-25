from flask import request
from exceptions.error_types.http_not_found import NotFoundError
from models.schemas.auth.post.forgot_password import ForgotPasswordRequest
from models.usuario import Usuario
from templates.email_templates import reset_password_email_template
from utils.functions import is_valid_email
from utils.send_email import send_email
from utils.token_email import generate_token


class ForgotPassword:
    def execute(self):
        req = ForgotPasswordRequest.parse_obj(request.get_json())
        email = is_valid_email(
            req.email.strip(), check_deliverability=False, check_valid_domain=False
        )
        url_redirect = req.url_redirect.strip()

        user = self.__search_user_email(email)
        self.__send_reset_password_email(email, user.nome, url_redirect)
        return {"msg": "Email enviado com sucesso."}, 200

    def __search_user_email(self, email: str) -> Usuario:
        user: Usuario = Usuario.query.filter_by(email=email, deleted_at=None).first()
        if user is None:
            raise NotFoundError(
                "Lamentamos que não foi possível identificá-lo segundo as informações fornecidas."
            )
        return user

    def __send_reset_password_email(self, email: str, user_name: str, url_redirect) -> None:
        token = generate_token(obj=email, salt="reset_password_confirmation")
        html = reset_password_email_template(user_name, token, url_redirect)
        send_email("HeSed - Confirmação de redefinição de senha", email, html, 2)
