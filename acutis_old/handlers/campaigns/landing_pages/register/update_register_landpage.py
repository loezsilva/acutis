from flask import request, json
from models import Clifor, Usuario, Endereco, Campanha, FotoCampanha
from builder import db
from validate_docbr import CPF
import logging
from services.factories import file_service_factory
from utils.functions import get_current_time
from utils.regex import format_string
from exceptions.error_types.http_not_found import NotFoundError


class UpdateRegisterLandPage:

    def __init__(self) -> None:
        pass

    def execute(self):
        try:
            data = json.loads(request.form.get("data"))

            self.__name = data["nome"].strip()
            self.__country = data["pais"].strip()
            self.__cpf_cnpj = data["cpf"]
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

            if self.__country == True and self.__brasileiro:
                self.__validate_cpf()

            clifor: Clifor = self.__get_clifor()

            if clifor is None:
                raise NotFoundError("Usuário não encontrado")

            s3_client = file_service_factory()
            usuario: Usuario = self.__get_user(clifor.fk_usuario_id)
            endereco: Endereco = self.__get_endereco(clifor.id)
            campanha: Campanha = self.__get_campaign(self.__fk_campanha_id)

            usuario.nome = self.__name
            usuario.obriga_atualizar_cadastro = False
            usuario.data_alteracao = get_current_time()
            usuario.usuario_alteracao = usuario.id
            usuario.country = self.__country

            clifor.nome = self.__name
            clifor.data_nascimento = self.__data_nascimento
            clifor.sexo = self.__sexo
            clifor.data_alteracao = get_current_time()
            clifor.usuario_alteracao = usuario.id

            endereco.rua = self.__rua
            endereco.complemento = self.__complemento
            endereco.numero = self.__numero
            endereco.bairro = self.__bairro
            endereco.cidade = self.__cidade
            endereco.estado = self.__estado
            endereco.cep = self.__cep
            endereco.ultima_atualizacao_endereco = get_current_time()
            endereco.data_alteracao = get_current_time()
            endereco.usuario_alteracao = usuario.id
            endereco.detalhe_estrangeiro = self.__detalhe_estrangeiro

            if campanha and campanha.preenchimento_foto:
                image_file = request.files.get("image")
                if image_file is None:
                    raise NotFoundError("O envio da foto é obrigatório.")

                nome_usuario = format_string(self.__name)
                filename = f"{self.__fk_campanha_id}_{usuario.id}_{'_'.join(nome_usuario.split(' '))}.jpg"

                foto_campanha = FotoCampanha.query.filter_by(
                    fk_usuario_id=usuario.id,
                    fk_campanha_id=self.__fk_campanha_id,
                ).first()

                if foto_campanha is None:
                    s3_client.upload_image(image_file, filename)

                    foto_campanha = FotoCampanha(
                        fk_campanha_id=self.__fk_campanha_id,
                        fk_usuario_id=usuario.id,
                        foto=filename,
                        usuario_criacao=usuario.id,
                    )
                    db.session.add(foto_campanha)
                else:
                    s3_client.delete_object(
                        s3_path=f"homolog/{foto_campanha.foto}"
                    )
                    s3_client.upload_image(image_file, filename)

                    foto_campanha.foto = filename
                    foto_campanha.data_alteracao = get_current_time()
                    foto_campanha.usuario_alteracao = usuario.id

            db.session.commit()

            return {"msg": "Registro atualizado com sucesso!"}, 200

        except Exception as err:
            db.session.rollback()
            logging.error(f"Error ao atualizar usuário! - {type(err)} - {err}")
            return {"error": "Error ao atualizar usuário!"}, 500

    def __validate_cpf(self):
        cpf_validator = CPF()
        if not cpf_validator.validate(self.__cpf_cnpj):
            return {"error": "CPF inválido!"}, 400
        return True

    def __get_clifor(self):
        clifor: Clifor = Clifor.query.filter_by(
            cpf_cnpj=self.__cpf_cnpj
        ).first()
        return clifor

    def __get_user(self, clifor_id):
        usuario: Usuario = Usuario.query.filter_by(id=clifor_id).first()
        return usuario

    def __get_endereco(self, clifor_id):
        endereco: Endereco = Endereco.query.filter_by(
            fk_clifor_id=clifor_id
        ).first()
        return endereco

    def __get_campaign(self, campanha_id):
        campanha: Campanha = Campanha.query.filter_by(id=campanha_id).first()
        return campanha
