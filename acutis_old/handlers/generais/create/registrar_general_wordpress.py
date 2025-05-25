from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from models.campanha import Campanha
from models.endereco import Endereco
from models.generais import Generais
from models.landpage_usuarios import LandpageUsers
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from models.clifor import Clifor
from models.schemas.admin.post.register_general import FormGeneralWordPressRequest
from utils.functions import get_current_time, is_valid_birthdate, is_valid_email, is_valid_name
from utils.regex import format_string, validate_password
from utils.validator import cpf_cnpj_validator


class RegisterGeneralWordPress:
    def __init__(
        self,
        database: SQLAlchemy,
        register_usuario_deletado_usecase,
        register_usuario_anonimo_use_case,
    ):

        self.__database = database
        self.__register_usuario_deletado_usecase = register_usuario_deletado_usecase
        self.__register_usuario_anonimo_use_case = register_usuario_anonimo_use_case

    def execute(self):
        dados_da_requisicao = FormGeneralWordPressRequest(
            fk_usuario_superior_id=flask_request.form.get("fk_usuario_superior_id"),
            pais=flask_request.form.get("pais", "brasil"),
            usuario=flask_request.form["usuario"],
            endereco=flask_request.form["endereco"],
        )
        
        self.__validate_request_data(dados_da_requisicao)

        busca_registro = self.__busca_registro_usuario(
            dados_da_requisicao.usuario.numero_documento
        )

        if busca_registro[0] == "usuario_deletado":
            self.__register_usuario_deletado_usecase.register(
                database=self.__database,
                file_service=None,
                usuario=busca_registro[2],
                clifor=busca_registro[1],
                request=dados_da_requisicao,
            )
            usuario = busca_registro[2]
            return self.__registra_general(usuario.id, dados_da_requisicao)

        if busca_registro[0] == "usuario_anonimo":
            self.__register_usuario_anonimo_use_case.register(
                database=self.__database,
                file_service=None,
                clifor=busca_registro[1],
                perfil=Perfil.query.filter(Perfil.nome.ilike("Benfeitor")).first(),
                request=dados_da_requisicao,   
                origem_cadastro=None,
            )
            clifor: Clifor = Clifor.query.filter(Clifor.id == busca_registro[1].id).first()
            return self.__registra_general(clifor.fk_usuario_id, dados_da_requisicao)

        if busca_registro[0] == "usuario_para_atualizar":
            clifor = busca_registro[1]
            usuario = busca_registro[2]
            endereco = (
                self.__database.session.query(Endereco)
                .filter(Endereco.fk_clifor_id == clifor.id)
                .first()
            )
            
            self.__atualiza_usuario(endereco, usuario, clifor, dados_da_requisicao)
           
            return self.__registra_general(usuario.id, dados_da_requisicao)

        if busca_registro[0] == "usuario_novo":
            usuario = self.__criar_usuario(dados_da_requisicao)
            return self.__registra_general(usuario.id, dados_da_requisicao)

    def __busca_registro_usuario(self, numero_documento: str):

        clifor = Clifor.query.filter_by(cpf_cnpj=numero_documento).first()
        if clifor:
            if clifor.fk_usuario_id:
                usuario = self.__database.session.get(Usuario, clifor.fk_usuario_id)
                if usuario.deleted_at is not None:
                    return ("usuario_deletado", clifor, usuario)

                return ("usuario_para_atualizar", clifor, usuario)

            return ("usuario_anonimo", clifor)
        return ("usuario_novo",)

    def __atualiza_usuario(
        self,
        endereco_para_atualizar: Endereco,
        usuario: Usuario,
        clifor: Clifor,
        dados_para_atualizar: FormGeneralWordPressRequest,
    ) -> Usuario:

        if dados_para_atualizar.endereco is None:
            raise BadRequestError("O preenchimento do endereço é obrigatório.")
        
        if endereco_para_atualizar is None:
            endereco = Endereco(
                fk_clifor_id=clifor.id,
                rua=dados_para_atualizar.endereco.rua,
                numero= dados_para_atualizar.endereco.numero,
                complemento=dados_para_atualizar.endereco.complemento,
                ponto_referencia=dados_para_atualizar.endereco.ponto_referencia,
                bairro=dados_para_atualizar.endereco.bairro,
                cidade=dados_para_atualizar.endereco.cidade,
                estado=dados_para_atualizar.endereco.estado,
                cep=dados_para_atualizar.endereco.cep,
                detalhe_estrangeiro=dados_para_atualizar.endereco.detalhe_estrangeiro,
                pais_origem=dados_para_atualizar.pais,
                ultima_atualizacao_endereco=get_current_time().date(),
                usuario_criacao=usuario.id,
            )
            self.__database.session.add(endereco)
        else:
            endereco_para_atualizar.cep = dados_para_atualizar.endereco.cep
            endereco_para_atualizar.rua = dados_para_atualizar.endereco.rua
            endereco_para_atualizar.numero = dados_para_atualizar.endereco.numero
            endereco_para_atualizar.complemento = dados_para_atualizar.endereco.complemento
            endereco_para_atualizar.bairro = dados_para_atualizar.endereco.bairro
            endereco_para_atualizar.estado = dados_para_atualizar.endereco.estado
            endereco_para_atualizar.cidade = dados_para_atualizar.endereco.cidade
            endereco_para_atualizar.ponto_referencia = dados_para_atualizar.endereco.ponto_referencia
            endereco_para_atualizar.detalhe_estrangeiro = (
                dados_para_atualizar.endereco.detalhe_estrangeiro
            )
            endereco_para_atualizar.obriga_atualizar_endereco = False
            endereco_para_atualizar.ultima_atualizacao_endereco = get_current_time().date()
            endereco_para_atualizar.usuario_alteracao = usuario.id
            endereco_para_atualizar.data_alteracao = get_current_time()

        usuario.campanha_origem = dados_para_atualizar.usuario.campanha_origem
        # clifor.nome = dados_para_atualizar.usuario.nome
        # clifor.data_nascimento = dados_para_atualizar.usuario.data_nascimento
        # clifor.telefone1 = dados_para_atualizar.usuario.telefone
        # clifor.data_alteracao = get_current_time()
        # clifor.usuario_alteracao = usuario.id
        # clifor.sexo = dados_para_atualizar.usuario.sexo

        # usuario.nome = dados_para_atualizar.usuario.nome
        # usuario.data_alteracao = get_current_time()
        # usuario.usuario_alteracao = usuario.id
        # usuario.obriga_atualizar_cadastro = False

        self.__database.session.commit()

        return usuario

    def __criar_usuario(
        self, dados_da_requisicao: FormGeneralWordPressRequest
    ) -> Usuario:

        email_em_usuario = (
            self.__database.session.query(Usuario.email)
            .filter(Usuario.email == dados_da_requisicao.usuario.email)
            .first()
        )

        if email_em_usuario is not None:
            raise ConflictError("Email já cadastrado")
        
        self.__validate_telefone(dados_da_requisicao.usuario.telefone)

        novo_usuario = Usuario(
            nome=dados_da_requisicao.usuario.nome,
            nome_social=dados_da_requisicao.usuario.nome_social,
            email=dados_da_requisicao.usuario.email,
            password=dados_da_requisicao.usuario.password,
            country=dados_da_requisicao.pais,
            campanha_origem=dados_da_requisicao.usuario.campanha_origem,
            data_inicio=get_current_time(),
        )

        self.__database.session.add(novo_usuario)
        self.__database.session.flush()

        clifor = Clifor(
            fk_usuario_id=novo_usuario.id,
            nome=dados_da_requisicao.usuario.nome,
            cpf_cnpj=dados_da_requisicao.usuario.numero_documento,
            email=dados_da_requisicao.usuario.email,
            data_nascimento=dados_da_requisicao.usuario.data_nascimento,
            usuario_criacao=novo_usuario.id,
            telefone1=dados_da_requisicao.usuario.telefone,
            sexo=dados_da_requisicao.usuario.sexo,
        )
        self.__database.session.add(clifor)
        self.__database.session.flush()

        novo_endereco = Endereco(
            fk_clifor_id=clifor.id,
            rua=dados_da_requisicao.endereco.rua,
            numero=dados_da_requisicao.endereco.numero,
            complemento=dados_da_requisicao.endereco.complemento,
            ponto_referencia=dados_da_requisicao.endereco.ponto_referencia,
            bairro=dados_da_requisicao.endereco.bairro,
            cidade=dados_da_requisicao.endereco.cidade,
            estado=dados_da_requisicao.endereco.estado,
            cep=dados_da_requisicao.endereco.cep,
            detalhe_estrangeiro=dados_da_requisicao.endereco.detalhe_estrangeiro,
            pais_origem=dados_da_requisicao.pais,
            obriga_atualizar_endereco=True if not dados_da_requisicao.pais else False,
        )
        self.__database.session.add(novo_endereco)
        self.__database.session.flush()

        registra_permissao = PermissaoUsuario(
            fk_usuario_id=novo_usuario.id,
            fk_perfil_id=2,
            usuario_criacao=novo_usuario.id,
        )
        self.__database.session.add(registra_permissao)
        self.__database.session.flush()

        if dados_da_requisicao.usuario.campanha_origem is not None:
            campanha = self.__database.session.get(
                Campanha, dados_da_requisicao.usuario.campanha_origem
            )
            if campanha:
                landpage = campanha.landpage.first()
                if landpage:
                    landpage_user = LandpageUsers(
                        user_id=clifor.fk_usuario_id,
                        landpage_id=landpage.id,
                        campaign_id=campanha.id,
                        clifor_id=clifor.id,
                    )
                    self.__database.session.add(landpage_user)

        return novo_usuario

    def __registra_general(
        self, fk_usuario_id: int, dados_da_requisicao: FormGeneralWordPressRequest
    ) -> dict:

        general_ja_registrado: Generais = (
            self.__database.session.query(Generais)
            .filter(Generais.fk_usuario_id == fk_usuario_id)
            .first()
        )

        if general_ja_registrado is not None:
            general_ja_registrado.updated_at = get_current_time()
            general_ja_registrado.usuario_alteracao = fk_usuario_id
            general_ja_registrado.deleted_at = None

        else:
            novo_general = Generais(
                fk_usuario_id=fk_usuario_id,
                fk_cargo_id=2,
                status=0,
                fk_usuario_superior_id=dados_da_requisicao.fk_usuario_superior_id,
            )

            self.__database.session.add(novo_general)

        self.__database.session.commit()

        return {"msg": "Ação realizada com sucesso"}
    
    
    def __validate_request_data(
        self, request: FormGeneralWordPressRequest
    ) -> None:
        if request.pais.lower() == "brasil":
            campos_endereco = [
                request.endereco.cep,
                request.endereco.rua,
                request.endereco.numero,
                request.endereco.bairro,
                request.endereco.estado,
                request.endereco.cidade,
            ]
            preenchimento_completo_endereco_brasileiro = all(
                campo is not None for campo in campos_endereco
            )
            if not preenchimento_completo_endereco_brasileiro:
                raise BadRequestError(
                    "O preenchimento completo do endereço é obrigatório."
                )

        elif (
            request.pais.lower() != "brasil"
            and request.endereco.detalhe_estrangeiro is None
        ):
            raise BadRequestError(
                "O preenchimento completo do endereço de estrangeiro é obrigatório."
            )

        request.endereco.cep = format_string(
            request.endereco.cep, only_digits=True
        )
        request.usuario.numero_documento = cpf_cnpj_validator(
            request.usuario.numero_documento, request.usuario.tipo_documento
        )
        request.usuario.nome = is_valid_name(request.usuario.nome.strip())
        request.usuario.nome_social = is_valid_name(
            request.usuario.nome_social
        )
        request.usuario.data_nascimento = is_valid_birthdate(
            request.usuario.data_nascimento
        )
        request.usuario.email = is_valid_email(
            request.usuario.email.strip(),
            check_deliverability=True,
            check_valid_domain=False,
        )
        request.usuario.password = validate_password(
            request.usuario.password.get_secret_value()
        )
        request.usuario.telefone = format_string(
            request.usuario.telefone.strip(), only_digits=True
        )
        
        
    def __validate_telefone(self, telefone):
        telefone_formatado = format_string(
            telefone.strip(), only_digits=True
        )
        telefone_cadastrado = Clifor.query.filter_by(telefone1=telefone_formatado).first()
        if telefone_cadastrado is not None:
            raise ConflictError("Telefone já cadastrado")
        return telefone_formatado
