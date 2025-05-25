from datetime import date
from typing import Literal
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token

from builder import db
from models.endereco import Endereco
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from templates.email_templates import active_account_email_template
from utils.functions import get_current_time
from utils.regex import format_string
from utils.send_email import send_email
from utils.token_email import generate_token


class UpdateUserDeleted:
    def __init__(self, usuario, clifor) -> None:
        self.__usuario = usuario
        self.__clifor = clifor

    def execute(self, screen: Literal["Register", "Checkout"], payload=None):
        match screen:
            case "Register":
                return self.__update_user_deleted_screen_register()

            case "Checkout":
                return self.__update_user_deleted_screen_checkout(payload)

    def __update_user_deleted_screen_register(self):
        payload = request.get_json()

        nome = payload["name"].strip()
        email = payload["email"].strip()
        country = payload.get("pais")
        password = payload["password"].strip()

        if self.__validate_email_in_use(email):
            return {"error": "Email já cadastrado."}, 409

        self.__usuario.nome = nome
        self.__usuario.email = email
        self.__usuario.password = password
        self.__usuario.country = country
        self.__usuario.status = False
        self.__usuario.deleted_at = None
        self.__usuario.data_criacao = get_current_time

        self.__clifor.nome = nome
        self.__clifor.email = email

        self.__send_email_confirmation_account(email, nome)

        db.session.commit()

        return {"msg": "Usuário cadastrado com sucesso."}, 201

    def __update_user_deleted_screen_checkout(self, payload):
        nome = payload["nome"].strip()
        email = payload["email"].strip()
        password = payload["password"].strip()
        data_nascimento = payload.get("data_nascimento")
        sexo = payload.get("sexo")
        country = payload["pais"]

        cep = format_string(text=payload["cep"].strip(), only_digits=True)
        rua = payload["rua"].strip()
        complemento = payload.get("complemento")
        numero = payload["numero"].strip()
        bairro = payload["bairro"].strip()
        cidade = payload["cidade"].strip()
        estado = payload["estado"].strip()

        if self.__validate_email_in_use(email):
            return {"error": "Email já cadastrado."}, 409

        self.__usuario.nome = nome
        self.__usuario.email = email
        self.__usuario.password = password
        self.__usuario.country = country
        self.__usuario.status = False
        self.__usuario.deleted_at = None
        self.__usuario.data_criacao = get_current_time()

        self.__clifor.nome = nome
        self.__clifor.email = email
        self.__clifor.data_nascimento = data_nascimento
        self.__clifor.sexo = sexo

        endereco = Endereco.query.filter_by(
            fk_clifor_id=self.__clifor.id
        ).first()
        if endereco is None:
            address = Endereco(
                fk_clifor_id=self.__clifor.id,
                rua=rua,
                numero=numero,
                bairro=bairro,
                complemento=complemento,
                cidade=cidade,
                estado=estado,
                cep=cep,
                ultima_atualizacao_endereco=date.today(),
                usuario_criacao=self.__usuario.id,
                pais_origem="brasil",
            )
            db.session.add(address)
        else:
            endereco.rua = rua
            endereco.numero = numero
            endereco.bairro = bairro
            endereco.complemento = complemento
            endereco.cidade = cidade
            endereco.estado = estado
            endereco.cep = cep
            endereco.ultima_atualizacao_endereco = date.today()

        self.__send_email_confirmation_account(email, nome)

        db.session.commit()

        return {
            "msg": "Usuário cadastrado com sucesso.",
            "access_token": create_access_token(identity=self.__usuario.id),
            "refresh_token": create_refresh_token(identity=self.__usuario.id),
            "type_token": "Bearer",
        }, 201

    def __validate_email_in_use(self, email):
        valid_email = Usuario.query.filter_by(email=email).first()
        if valid_email and valid_email.id != self.__usuario.id:
            return True

        return False

    def __send_email_confirmation_account(self, email, name):
        payload = {"email": email}
        token = generate_token(obj=payload, salt="active_account_confirmation")
        html = active_account_email_template(name, token)
        send_email("HeSed - Verificação de Email", email, html, 1)
