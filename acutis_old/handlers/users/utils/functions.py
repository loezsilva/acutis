from typing import Optional

from models.schemas.users.post.register_user_full import RedirectPagesEnum
from models.usuario import Usuario
from templates.email_templates import (
    active_account_alistamento_email_template,
    active_account_email_template,
)
from utils.send_email import send_email
from utils.token_email import generate_token


def choose_template_active_account_to_send(
    db_usuario: Usuario,
    usuario: Usuario,
    pais: str,
    pagina_redirecionamento: Optional[RedirectPagesEnum],
) -> None:
    template_email = {
        RedirectPagesEnum.MEMBRO_EXERCITO: {
            "template": active_account_alistamento_email_template,
            "payload": {
                "nome": usuario.nome,
                "email": usuario.email,
                "telefone": usuario.telefone,
                "usuario_id": db_usuario.id,
                "pais": pais,
                "tipo_cadastro": "alistamento",
            },
        },
        RedirectPagesEnum.PRINCIPAL: {
            "template": active_account_email_template,
            "payload": {"email": usuario.email},
        },
    }

    token = generate_token(
        obj=template_email[pagina_redirecionamento]["payload"],
        salt="active_account_confirmation",
    )
    html = template_email[pagina_redirecionamento]["template"](
        usuario.nome, token
    )
    send_email("HeSed - Verificação de Email", usuario.email, html, 1)
