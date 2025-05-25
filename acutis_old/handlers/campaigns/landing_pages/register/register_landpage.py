from services.factories import file_service_factory
from services.send_data_to_app_acutis import SendDataToAppAcutis
from utils.functions import get_current_time
from builder import db
from models import (
    Clifor,
    Usuario,
    Campanha,
    Endereco,
    Perfil,
    LandpageUsers,
    FotoCampanha,
    PermissaoUsuario,
    EventoUsuario,
    LandPage,
)
from flask import request, json, jsonify
from exceptions.errors_handler import errors_handler
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_not_found import NotFoundError
from validate_docbr import CPF
from email_validator import validate_email
from utils.regex import validate_password, format_string
from handlers.users.put.update_user_deleted import UpdateUserDeleted
from utils.token_email import generate_token
from templates import active_account_email_template
from utils.send_email import send_email
import logging
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)


class RegisterLandPage:
    def __init__(self) -> any:
        self.__image = request.files.get("image")
        self.__s3_cliet = file_service_factory()

    def execute(self):

        try:
            return self.__process_request()
        except Exception as exception:
            error_response = errors_handler(exception)
            return error_response

    def __process_request(self):
        data = json.loads(request.form.get("data"))
        self.__anonymous_client = False

        self.__email = data["email"]
        self.__password = data["password"]
        self.__name = data["nome"].strip()
        self.__country = data["pais"].strip()
        self.__cpf = data["cpf"]
        self.__tipo_clifor = data["tipo_clifor"]
        self.__telefone = data["telefone"]
        self.__sexo = data["sexo"]
        self.__data_nascimento = data["data_nascimento"]
        self.__cep = data.get("cep")
        self.__estado = data.get("estado")
        self.__cidade = data.get("cidade")
        self.__bairro = data.get("bairro")
        self.__rua = data.get("rua")
        self.__numero = data.get("numero")
        self.__complemento = data.get("complemento")
        self.__brasileiro = data["brasileiro"]
        self.__fk_campanha_id = data.get("fk_campanha_id")
        self.__detalhe_estrangeiro = data.get("detalhe_estrangeiro")

        self.__validate_email(self.__email)
        self.__validate_password(self.__password)

        if self.__brasileiro == True:
            self.__validate_cpf(self.__cpf)

        # caso clifor exista e usuario for deletado reativa cadastro de usuário.
        clifor: Clifor = self.__is_clifor(self.__cpf)

        if self.__brasileiro or clifor:
            if clifor and clifor.fk_usuario_id:
                user: Usuario = self.__is_user(clifor.fk_usuario_id)
                if user and user.deleted_at != None:
                    use_case = UpdateUserDeleted(user, clifor)
                    return use_case.execute("Checkout", data)
                raise ConflictError("CPF já cadastrado.")

            if clifor and clifor.fk_usuario_id == None:
                self.__anonymous_client = True

        if self.__fk_campanha_id:
            self.__campaign: Campanha = self.__validate_campaign(
                self.__fk_campanha_id
            )

        else:
            self.__campaign: Campanha = None

        return self.__insert_usuario_in_db()

    def __validate_cpf(self, cpf: str):

        if len(cpf) == 11:
            validate_cpf = CPF()
            if not validate_cpf.validate(cpf):
                raise BadRequestError("CPF inválido")
        else:
            raise BadRequestError("CPF inválido")

    def __is_clifor(self, cpf_cnpj):
        get_clifor = Clifor.query.filter_by(cpf_cnpj=cpf_cnpj).first()
        return get_clifor

    def __is_user(self, fk_usuario_id):
        get_usuario = Usuario.query.filter_by(id=fk_usuario_id).first()
        return get_usuario

    def __validate_campaign(self, fk_campanha_id):
        campanha = Campanha.query.filter_by(id=fk_campanha_id).first()
        if campanha is None:
            raise BadRequestError("Campanha inválida")
        return campanha

    def __validate_email(self, email):
        validate_email(email)
        email = Usuario.query.filter_by(email=email, deleted_at=None).first()
        if email is not None:
            raise ConflictError("Email já cadastrado")
        return email

    def __validate_password(self, password):
        try:
            validate_password(password)
        except Exception:
            raise BadRequestError("Senha não pode ter espaços em branco!")

    def __get_profile(self, profile_id):
        profile = Perfil.query.filter_by(id=profile_id).first()

        if profile is None:
            raise NotFoundError("Perfil não encontrado")

        return profile

    def __validate_landpage(self):
        landpage = LandPage.query.filter_by(
            campanha_id=self.__fk_campanha_id
        ).first()
        return landpage

    def __send_email_verification(self, email, name):
        payload = {"email": email}
        token = generate_token(obj=payload, salt="active_account_confirmation")
        html = active_account_email_template(name, token)
        send_email("HeSed - Verificação de Email", email, html, 1)

    def __format_response(self, user):
        return {
            "msg": "Usuário cadastrado com sucesso.",
            "access_token": create_access_token(identity=user.id),
            "refresh_token": create_refresh_token(identity=user.id),
            "type_token": "Bearer",
        }, 201

    def __insert_usuario_in_db(self):
        try:
            self.__validate_telefone(self.__telefone)
            
            profile = self.__get_profile(2)

            clifor = self.__is_clifor(self.__cpf)

            landpage = self.__validate_landpage()
            
            if clifor != None:
                fk_clifor_id = clifor.id
            else:
                fk_clifor_id = None

            new_user = Usuario(
                email=self.__email,
                password=self.__password,
                campanha_origem=(
                    self.__fk_campanha_id if self.__fk_campanha_id else None
                ),
                data_inicio=get_current_time(),
                country=self.__country,
                nome=self.__name,
            )

            db.session.add(new_user)
            db.session.flush()

            if self.__anonymous_client:
                clifor.cpf_cnpj = self.__cpf
                clifor.nome = self.__name
                clifor.fk_empresa_id = 1
                clifor.fk_usuario_id = new_user.id
                clifor.tipo_clifor = self.__tipo_clifor
                clifor.data_nascimento = self.__data_nascimento
                clifor.sexo = self.__sexo
                clifor.email = self.__email
                clifor.usuario_criacao = new_user.id
            else:
                new_clifor = Clifor(
                    cpf_cnpj=self.__cpf,
                    nome=self.__name,
                    fk_empresa_id=1,
                    fk_usuario_id=new_user.id,
                    tipo_clifor=self.__tipo_clifor,
                    data_nascimento=self.__data_nascimento,
                    sexo=self.__sexo,
                    email=self.__email,
                    telefone1=self.__telefone,
                    usuario_criacao=new_user.id,
                )

                db.session.add(new_clifor)
                db.session.flush()

            if self.__brasileiro:
                address = Endereco(
                    fk_clifor_id=(
                        fk_clifor_id if fk_clifor_id else new_clifor.id
                    ),
                    rua=self.__rua,
                    numero=self.__numero,
                    bairro=self.__bairro,
                    complemento=self.__complemento,
                    cidade=self.__cidade,
                    estado=self.__estado,
                    cep=self.__cep,
                    ultima_atualizacao_endereco=get_current_time(),
                    usuario_criacao=new_user.id,
                    pais_origem=self.__country,
                )
            else:
                address = Endereco(
                    fk_clifor_id=(
                        fk_clifor_id if fk_clifor_id else new_clifor.id
                    ),
                    detalhe_estrangeiro=self.__detalhe_estrangeiro,
                    pais_origem=self.__country,
                    ultima_atualizacao_endereco=get_current_time(),
                    usuario_criacao=new_user.id,
                )

            db.session.add(address)
            db.session.flush()

            user_permissions = PermissaoUsuario(
                fk_empresa_id=1,
                fk_usuario_id=new_user.id,
                fk_sistema_id=profile.fk_sistema_id,
                fk_perfil_id=profile.id,
                usuario_criacao=new_user.id,
            )
            db.session.add(user_permissions)
            db.session.flush()

            landpage_track = LandpageUsers(
                user_id=new_user.id,
                clifor_id=fk_clifor_id if fk_clifor_id else new_clifor.id,
                landpage_id=landpage.id if landpage else None,
                campaign_id=self.__fk_campanha_id,
                registered_at=get_current_time(),
            )
            db.session.add(landpage_track)
            db.session.flush()

            new_register = EventoUsuario(
                fk_usuario_id=new_user.id,
                fk_campanha_id=self.__fk_campanha_id,
                data_register=get_current_time(),
                presencas=1,
            )
            db.session.add(new_register)
            db.session.flush()

            if self.__campaign and self.__campaign.preenchimento_foto:
                image_data = self.__image
                if image_data is None:
                    return {"error": "O envio da foto é obrigatório."}, 400

                nome_usuario = format_string(self.__name)
                filename = f"{self.__fk_campanha_id}_{new_user.id}_{'**_'.join(nome_usuario.split(' '))}"

                self.__s3_cliet.upload_image(image_data, filename)

                foto_campanha = FotoCampanha(
                    fk_campanha_id=self.__fk_campanha_id,
                    fk_usuario_id=new_user.id,
                    foto=filename,
                    usuario_criacao=new_user.id,
                )
                db.session.add(foto_campanha)
                db.session.flush()

            db.session.commit()

            self.__send_email_verification(
                self.__email, self.__name
            )
            
            if self.__fk_campanha_id == 43:
                # envia dados do usuário para o app acutis quando presença registrada na campanha 43
                payload = {
                    "email": self.__email,
                    "cpf": self.__cpf,
                    "patent": "membro",
                    "name": self.__name
                }
                            
                register_general_in_app_acutis = SendDataToAppAcutis(payload)
                register_general_in_app_acutis.execute()

            return self.__format_response(new_user)

        except Exception as err:
            db.session.rollback()
            return (
                jsonify(
                    error="Ocorreu um erro ao cadastrar o usuário.",
                    type_error=str(type(err)),
                    msg_error=str(err),
                ),
                500,
            )


    def __validate_telefone(self, telefone):
        telefone_formatado = format_string(
            telefone.strip(), only_digits=True
        )
        telefone_cadastrado = Clifor.query.filter_by(telefone1=telefone_formatado).first()
        if telefone_cadastrado is not None:
            raise ConflictError("Telefone já cadastrado")
        return telefone_formatado